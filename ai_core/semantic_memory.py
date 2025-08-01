"""Semantic episodic memory module backed by SQLite.

文件结构说明：

```
SemanticMemory -> 核心类
  _embed()     -> 文本或句向量嵌入函数
  add_memory() -> 存入对话记录并更新索引
  query_memory() -> 使用向量搜索相似内容
```
"""

import datetime
import hashlib
import logging
import json
import os
import sqlite3
from typing import List, Dict, Any

try:
    import numpy as np  # type: ignore
except ImportError:  # pragma: no cover
    np = None


from .constants import (
    LOG_LEVEL,
    DEFAULT_MEMORY_SAVE_URL,
    DEFAULT_MEMORY_QUERY_URL,
    MEMORY_DB_PATH,
)
from .service_api import call_memory_save, call_memory_query

try:
    from sentence_transformers import SentenceTransformer  # type: ignore
except Exception:  # pragma: no cover - library missing
    SentenceTransformer = None

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)


class SemanticMemory:
    """Simple vector-based semantic memory using SQLite.

    基于向量的语义记忆模块，使用 SQLite 数据库存储记录。
    """

    def __init__(
        self,
        vector_dim: int = 384,
        save_url: str | None = DEFAULT_MEMORY_SAVE_URL,
        query_url: str | None = DEFAULT_MEMORY_QUERY_URL,
        use_transformer: bool | None = None,
        model_name: str = "all-MiniLM-L6-v2",
        db_path: str = MEMORY_DB_PATH,
    ) -> None:
        """Initialize memory store backed by SQLite.

        初始化基于 SQLite 的记忆存储。

        Parameters
        ----------
        vector_dim: int, optional
            Dimensionality of embedding vectors. 嵌入向量的维度，默认为 ``384``。
        save_url: str | None, optional
            Remote service to store memory records. 记忆存储服务地址。
        query_url: str | None, optional
            Remote service to query memory records. 记忆查询服务地址。
        db_path: str, optional
            Path to the SQLite database storing memory records.
            记忆记录保存的 SQLite 数据库路径。
        """
        self.vector_dim = vector_dim  # 向量维度
        self.records: List[Dict[str, Any]] = []  # 存储对话记录
        self.save_url = save_url
        self.query_url = query_url
        self.transformer = None
        if use_transformer is None:
            use_transformer = SentenceTransformer is not None
        if use_transformer and SentenceTransformer is not None:
            try:
                self.transformer = SentenceTransformer(model_name)
                test_vec = self.transformer.encode(["test"])[0]
                self.vector_dim = len(test_vec)
            except Exception as exc:  # pragma: no cover
                logger.warning("SentenceTransformer load failed: %s", exc)
                self.transformer = None
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_db()
        self.load()

    def _init_db(self) -> None:
        """Create the memory table if it doesn't exist."""
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS memory (
                time TEXT,
                user_text TEXT,
                ai_response TEXT,
                mood_tag TEXT,
                user_id TEXT,
                touched INTEGER,
                touch_zone INTEGER,
                vector TEXT
            )
            """
        )
        self.conn.commit()

    def load(self) -> None:
        """Load records from the SQLite database into memory."""
        cur = self.conn.cursor()
        rows = cur.execute("SELECT * FROM memory").fetchall()
        self.records = []
        for row in rows:
            self.records.append(
                {
                    "time": datetime.datetime.fromisoformat(row["time"]),
                    "user_text": row["user_text"],
                    "ai_response": row["ai_response"],
                    "mood_tag": row["mood_tag"],
                    "user_id": row["user_id"],
                    "touched": bool(row["touched"]),
                    "touch_zone": row["touch_zone"],
                    "topic_vector": json.loads(row["vector"]),
                }
            )

    def _embed(self, text: str):
        """Convert text to a vector using sentence transformers when available.

        优先使用 ``sentence-transformers`` 生成真实语义向量，若库或模型缺失
        则退化为改进的哈希向量。"""

        logger.debug("Embedding text: %s", text)
        if self.transformer is not None:
            try:
                vec = self.transformer.encode([text])[0]
                if np is not None:
                    return np.array(vec, dtype="float32")
                return [float(v) for v in vec]
            except Exception as exc:  # pragma: no cover
                logger.warning("Transformer embedding failed: %s", exc)

        # 改进的哈希向量生成
        # 1. 分词处理
        words = text.lower().split()
        # 2. 生成词级别的哈希
        word_hashes = []
        for word in words:
            word_hash = hashlib.md5(word.encode("utf-8")).digest()
            word_hashes.extend([b / 255.0 for b in word_hash[:8]])
        
        # 3. 生成句子级别的哈希
        sentence_hash = hashlib.sha256(text.encode("utf-8")).digest()
        sentence_vec = [b / 255.0 for b in sentence_hash[:16]]
        
        # 4. 组合向量
        combined_vec = word_hashes + sentence_vec
        
        # 5. 调整到目标维度
        if len(combined_vec) < self.vector_dim:
            combined_vec += [0.0] * (self.vector_dim - len(combined_vec))
        else:
            combined_vec = combined_vec[:self.vector_dim]
        
        return combined_vec


    def add_memory(
        self,
        user_text: str,
        ai_response: str,
        mood_tag: str = "neutral",
        user_id: str = "unknown",
        touched: bool = False,
        touch_zone: int | None = None,
    ) -> None:
        """Add a conversation record into memory.

        新增一条对话记录到记忆库中。

        Parameters
        ----------
        user_text: str
            User input text.
        ai_response: str
            Reply generated by the system.
        mood_tag: str, optional
            Emotion label associated with the conversation. Defaults to
            ``"neutral"`` when unspecified.
            对应的情绪标签，默认值为 ``"neutral"``。
        touch_zone: int | None, optional
            Identifier for the touch sensor zone if a touch interaction
            occurred.  触摸传感器的区域编号，可为 ``None`` 表示无触摸。"""
        vec = self._embed(user_text)
        record = {
            "time": datetime.datetime.utcnow(),
            "user_text": user_text,
            "ai_response": ai_response,
            "mood_tag": mood_tag,
            "user_id": user_id,
            "touched": touched,
            "touch_zone": touch_zone,
            "topic_vector": vec,
        }
        self.records.append(record)
        
        # 增强记忆日志输出
        logger.info("💾 新增记忆记录")
        logger.info(f"   📝 用户输入: {user_text}")
        logger.info(f"   🤖 AI回复: {ai_response}")
        logger.info(f"   😊 情绪标签: {mood_tag}")
        logger.info(f"   👤 用户ID: {user_id}")
        logger.info(f"   🤗 触摸状态: {touched}")
        logger.info(f"   📍 触摸区域: {touch_zone}")
        logger.info(f"   📊 记忆总数: {len(self.records)}")
        
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO memory VALUES (?,?,?,?,?,?,?,?)",
            (
                record["time"].isoformat(),
                user_text,
                ai_response,
                mood_tag,
                user_id,
                int(touched),
                touch_zone,
                json.dumps(vec),
            ),
        )
        self.conn.commit()
        if self.save_url:
            ok = call_memory_save(record, self.save_url)
            if not ok:
                logger.info(
                    "Remote memory service failed; record kept locally.")
        
    def query_memory(
        self, prompt: str, top_k: int = 3, user_id: str | None = None
    ) -> List[Dict[str, Any]]:
        """Return most relevant past interactions for the prompt.

        根据提示查询最相关的历史对话。

        Parameters
        ----------
        prompt: str
            Query text used for retrieving memories.
        top_k: int, optional
            Number of records to return. 默认返回 3 条记录。
        user_id: str | None, optional
            If provided, filter memories belonging to this user.
            如提供该参数，则只返回该用户的历史记录。
        """
        query_vec = self._embed(prompt)
        logger.debug("Querying memory for: %s", prompt)
        if self.query_url:
            res = call_memory_query(prompt, top_k, self.query_url)
            if res is not None:
                return res
        candidates = [
            r for r in self.records if user_id is None or r.get("user_id") == user_id
        ]
        # 改进的相似度搜索
        def similarity(a, b):
            """计算余弦相似度"""
            dot_product = sum(x * y for x, y in zip(a, b))
            norm_a = sum(x * x for x in a) ** 0.5
            norm_b = sum(x * x for x in b) ** 0.5
            if norm_a == 0 or norm_b == 0:
                return 0
            return dot_product / (norm_a * norm_b)
        
        # 计算相似度分数
        scores = [similarity(r["topic_vector"], query_vec) for r in candidates]
        # 按相似度降序排序（相似度越高越好）
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
        results = [candidates[i] for i in top_indices]
        
        # 增强记忆查询日志输出
        logger.info("🔍 记忆查询结果")
        logger.info(f"   📝 查询内容: {prompt}")
        logger.info(f"   📊 候选记录数: {len(candidates)}")
        logger.info(f"   🎯 返回记录数: {len(results)}")
        if results:
            logger.info("   📋 相关记忆:")
            for i, result in enumerate(results, 1):
                logger.info(f"     {i}. 用户: {result['user_text']}")
                logger.info(f"        AI: {result['ai_response']}")
                logger.info(f"        情绪: {result['mood_tag']}")
                logger.info(f"        时间: {result['time']}")
        
        return results  # 返回按距离排序的结果

    def save_backup(self, path: str) -> None:
        """Save memory records to a JSON backup file.

        将记忆记录保存到 JSON 备份文件。
        """
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(self.records, fh, default=str, ensure_ascii=False)
        logger.info("Memory backup saved to %s", path)

    def load_backup(self, path: str) -> None:
        """Load memory records from a JSON backup file."""
        try:
            with open(path, "r", encoding="utf-8") as fh:
                self.records = json.load(fh)
        except FileNotFoundError:
            logger.warning("Memory file %s not found", path)
            self.records = []
        logger.info("Loaded %d memory records from backup", len(self.records))

    def last_mood(self, user_id: str | None = None) -> str | None:
        """Return the most recent mood tag for a user."""

        # 返回给定用户最近一次对话的情绪标签
        candidates = [r for r in self.records if user_id is None or r.get("user_id") == user_id]
        if not candidates:
            return None
        return candidates[-1].get("mood_tag")