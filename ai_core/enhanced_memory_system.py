"""Enhanced Memory System for Companion Robot

增强记忆系统，提供多层次、智能化的记忆管理。
包含短期记忆、长期记忆、上下文记忆和情感记忆。
"""

import datetime
import json
import logging
import sqlite3
import threading
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional, Tuple, Deque
from collections import deque
import hashlib
import uuid

try:
    import numpy as np
    from sentence_transformers import SentenceTransformer
except ImportError:
    np = None
    SentenceTransformer = None

from .constants import LOG_LEVEL
from ai_core.constants import HISTORY_MAX_RECORDS

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)


@dataclass
class MemoryRecord:
    """记忆记录数据结构"""
    id: str                           # 唯一标识
    robot_id: str                     # 机器人ID
    timestamp: datetime.datetime       # 时间戳
    user_text: str                    # 用户输入
    ai_response: str                  # AI回复
    mood_tag: str                     # 情绪标签
    touch_zone: Optional[int]         # 触摸区域
    context_id: str                   # 上下文ID
    session_id: str                   # 会话ID
    importance_score: float           # 重要性评分
    memory_type: str                  # 记忆类型
    vector: Optional[List[float]]     # 语义向量
    metadata: Dict[str, Any]         # 元数据


@dataclass
class ContextWindow:
    """上下文窗口数据结构"""
    session_id: str                   # 会话ID
    robot_id: str                     # 机器人ID
    records: Deque[MemoryRecord]      # 记忆记录队列
    max_size: int                     # 最大记录数
    current_context: str              # 当前上下文摘要
    emotion_trend: List[str]          # 情绪趋势
    interaction_count: int            # 交互次数


class EnhancedMemorySystem:
    """增强记忆系统
    
    提供多层次记忆管理：
    1. 短期记忆（会话记忆）
    2. 长期记忆（语义记忆）
    3. 上下文记忆（对话连续性）
    4. 情感记忆（情绪关联）
    """

    def __init__(
        self,
        robot_id: str,
        db_path: str = "enhanced_memory.db",
        session_limit: int = 20,
        context_window_size: int = 10,
        vector_dim: int = 384,
        model_name: str = "all-MiniLM-L6-v2",
    ):
        """初始化增强记忆系统
        
        Parameters
        ----------
        robot_id: str
            机器人ID
        db_path: str
            数据库路径
        session_limit: int
            会话记忆限制
        context_window_size: int
            上下文窗口大小
        vector_dim: int
            向量维度
        model_name: str
            向量模型名称
        """
        self.robot_id = robot_id
        self.db_path = db_path
        self.session_limit = session_limit
        self.context_window_size = context_window_size
        self.vector_dim = vector_dim
        
        # 初始化向量模型
        self.transformer = None
        if SentenceTransformer is not None:
            try:
                self.transformer = SentenceTransformer(model_name)
                test_vec = self.transformer.encode(["test"])[0]
                self.vector_dim = len(test_vec)
                logger.info(f"✅ 向量模型加载成功: {model_name}")
            except Exception as e:
                logger.warning(f"⚠️ 向量模型加载失败: {e}")
        
        # 初始化数据库
        self._init_database()
        
        # 会话记忆（短期记忆）
        self.session_memory = deque(maxlen=session_limit)
        
        # 上下文窗口
        self.context_windows: Dict[str, ContextWindow] = {}
        
        # 当前会话ID
        self.current_session_id = None
        
        # 线程锁，用于保护数据库操作
        self._db_lock = threading.Lock()
        
        logger.info(f"🔧 增强记忆系统初始化完成")
        logger.info(f"   🤖 机器人ID: {robot_id}")
        logger.info(f"   📊 会话限制: {session_limit}")
        logger.info(f"   🪟 上下文窗口: {context_window_size}")
        logger.info(f"   🧠 向量维度: {self.vector_dim}")
    
    def _init_database(self):
        """初始化数据库表结构"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        
        cursor = self.conn.cursor()
        
        # 创建记忆记录表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory_records (
                id TEXT PRIMARY KEY,
                robot_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                user_text TEXT NOT NULL,
                ai_response TEXT NOT NULL,
                mood_tag TEXT NOT NULL,
                touch_zone INTEGER,
                context_id TEXT NOT NULL,
                session_id TEXT NOT NULL,
                importance_score REAL NOT NULL,
                memory_type TEXT NOT NULL,
                vector TEXT,
                metadata TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 创建会话表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                robot_id TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT,
                interaction_count INTEGER DEFAULT 0,
                emotion_summary TEXT,
                context_summary TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 创建上下文表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contexts (
                context_id TEXT PRIMARY KEY,
                session_id TEXT NOT NULL,
                robot_id TEXT NOT NULL,
                context_summary TEXT,
                emotion_trend TEXT,
                record_count INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 创建索引
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_robot_id ON memory_records(robot_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_session_id ON memory_records(session_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_context_id ON memory_records(context_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON memory_records(timestamp)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_memory_type ON memory_records(memory_type)")
        
        self.conn.commit()
        logger.info("✅ 数据库初始化完成")
    
    def _embed_text(self, text: str) -> List[float]:
        """文本向量化"""
        if self.transformer is None:
            # 如果没有向量模型，返回随机向量
            import random
            return [random.random() for _ in range(self.vector_dim)]
        
        try:
            vector = self.transformer.encode([text])[0]
            return vector.tolist()
        except Exception as e:
            logger.error(f"❌ 向量化失败: {e}")
            return [0.0] * self.vector_dim
    
    def _calculate_importance_score(
        self,
        user_text: str,
        ai_response: str,
        mood_tag: str,
        touch_zone: Optional[int],
        interaction_count: int,
    ) -> float:
        """计算记忆重要性评分"""
        score = 0.0
        
        # 基础分数
        score += 0.3
        
        # 文本长度影响
        text_length = len(user_text) + len(ai_response)
        score += min(text_length / 1000, 0.2)
        
        # 情绪影响
        emotion_scores = {
            "happy": 0.3,
            "excited": 0.4,
            "sad": 0.2,
            "angry": 0.3,
            "surprised": 0.3,
            "neutral": 0.1
        }
        score += emotion_scores.get(mood_tag, 0.1)
        
        # 触摸影响
        if touch_zone is not None:
            score += 0.2
        
        # 交互频率影响（早期交互更重要）
        if interaction_count <= 5:
            score += 0.3
        elif interaction_count <= 10:
            score += 0.1
        
        # 关键词检测
        important_keywords = [
            "喜欢", "讨厌", "重要", "记住", "忘记", "名字", "生日",
            "家", "朋友", "工作", "学习", "梦想", "目标"
        ]
        for keyword in important_keywords:
            if keyword in user_text or keyword in ai_response:
                score += 0.2
                break
        
        return min(score, 1.0)
    
    def start_session(self, session_id: Optional[str] = None) -> str:
        """开始新会话"""
        if session_id is None:
            session_id = str(uuid.uuid4())
        
        self.current_session_id = session_id
        
        # 创建上下文窗口
        context_window = ContextWindow(
            session_id=session_id,
            robot_id=self.robot_id,
            records=deque(maxlen=self.context_window_size),
            max_size=self.context_window_size,
            current_context="",
            emotion_trend=[],
            interaction_count=0
        )
        
        self.context_windows[session_id] = context_window
        
        # 记录到数据库
        with self._db_lock:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO sessions 
                (session_id, robot_id, start_time, interaction_count)
                VALUES (?, ?, ?, ?)
            """, (session_id, self.robot_id, datetime.datetime.utcnow().isoformat(), 0))
            self.conn.commit()
        
        logger.info(f"🆕 开始新会话: {session_id}")
        return session_id
    
    def add_memory(
        self,
        user_text: str,
        ai_response: str,
        mood_tag: str = "neutral",
        touch_zone: Optional[int] = None,
        session_id: Optional[str] = None,
        context_id: Optional[str] = None,
    ) -> str:
        """添加记忆记录"""
        if session_id is None:
            session_id = self.current_session_id or self.start_session()
        
        if context_id is None:
            context_id = str(uuid.uuid4())
        
        # 获取上下文窗口
        context_window = self.context_windows.get(session_id)
        if context_window is None:
            context_window = ContextWindow(
                session_id=session_id,
                robot_id=self.robot_id,
                records=deque(maxlen=self.context_window_size),
                max_size=self.context_window_size,
                current_context="",
                emotion_trend=[],
                interaction_count=0
            )
            self.context_windows[session_id] = context_window
        
        # 更新交互计数
        context_window.interaction_count += 1
        
        # 计算重要性评分
        importance_score = self._calculate_importance_score(
            user_text, ai_response, mood_tag, touch_zone, context_window.interaction_count
        )
        
        # 生成向量
        combined_text = f"{user_text} {ai_response}"
        vector = self._embed_text(combined_text)
        
        # 创建记忆记录
        memory_id = str(uuid.uuid4())
        record = MemoryRecord(
            id=memory_id,
            robot_id=self.robot_id,
            timestamp=datetime.datetime.utcnow(),
            user_text=user_text,
            ai_response=ai_response,
            mood_tag=mood_tag,
            touch_zone=touch_zone,
            context_id=context_id,
            session_id=session_id,
            importance_score=importance_score,
            memory_type="interaction",
            vector=vector,
            metadata={
                "interaction_count": context_window.interaction_count,
                "session_length": len(context_window.records) + 1
            }
        )
        
        # 添加到会话记忆
        context_window.records.append(record)
        context_window.emotion_trend.append(mood_tag)
        
        # 更新上下文摘要
        self._update_context_summary(context_window)
        
        # 存储到数据库
        self._save_memory_record(record)
        
        # 更新会话统计
        self._update_session_stats(session_id, context_window)
        
        logger.info(f"💾 添加记忆记录: {memory_id}")
        logger.info(f"   📝 用户: {user_text[:50]}...")
        logger.info(f"   🤖 AI: {ai_response[:50]}...")
        logger.info(f"   😊 情绪: {mood_tag}")
        logger.info(f"   ⭐ 重要性: {importance_score:.2f}")
        
        return memory_id
    
    def _save_memory_record(self, record: MemoryRecord):
        """保存记忆记录到数据库"""
        with self._db_lock:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO memory_records 
                (id, robot_id, timestamp, user_text, ai_response, mood_tag, 
                 touch_zone, context_id, session_id, importance_score, 
                 memory_type, vector, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                record.id,
                record.robot_id,
                record.timestamp.isoformat(),
                record.user_text,
                record.ai_response,
                record.mood_tag,
                record.touch_zone,
                record.context_id,
                record.session_id,
                record.importance_score,
                record.memory_type,
                json.dumps(record.vector) if record.vector else None,
                json.dumps(record.metadata)
            ))
            self.conn.commit()
    
    def _update_context_summary(self, context_window: ContextWindow):
        """更新上下文摘要"""
        if not context_window.records:
            return
        
        # 获取最近的记录
        recent_records = list(context_window.records)[-3:]
        
        # 构建上下文摘要
        summary_parts = []
        for record in recent_records:
            summary_parts.append(f"用户说'{record.user_text}'，我回复'{record.ai_response}'")
        
        context_window.current_context = "。".join(summary_parts) + "。"
        
        # 更新情绪趋势
        if len(context_window.emotion_trend) > 5:
            context_window.emotion_trend = context_window.emotion_trend[-5:]
    
    def _update_session_stats(self, session_id: str, context_window: ContextWindow):
        """更新会话统计信息"""
        with self._db_lock:
            cursor = self.conn.cursor()
            
            # 计算情绪摘要
            emotion_counts = {}
            for emotion in context_window.emotion_trend:
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            
            dominant_emotion = max(emotion_counts.items(), key=lambda x: x[1])[0] if emotion_counts else "neutral"
            
            cursor.execute("""
                UPDATE sessions 
                SET interaction_count = ?, emotion_summary = ?, context_summary = ?
                WHERE session_id = ?
            """, (
                context_window.interaction_count,
                dominant_emotion,
                context_window.current_context,
                session_id
            ))
            self.conn.commit()
    
    def query_memory(
        self,
        prompt: str,
        top_k: int = 5,
        session_id: Optional[str] = None,
        memory_types: Optional[List[str]] = None,
        use_context: bool = True,
    ) -> Dict[str, Any]:
        """查询相关记忆"""
        if memory_types is None:
            memory_types = ["interaction", "semantic", "emotional"]
        
        # 1. 查询语义相似记忆
        semantic_memories = self._query_semantic_memory(prompt, top_k)
        
        # 2. 查询上下文记忆
        context_memories = []
        if use_context and session_id:
            context_memories = self._query_context_memory(session_id, top_k)
        
        # 3. 查询情感相关记忆
        emotional_memories = self._query_emotional_memory(prompt, top_k)
        
        # 4. 融合记忆结果
        fused_memories = self._fuse_memories(
            semantic_memories, context_memories, emotional_memories, top_k
        )
        
        # 5. 生成记忆摘要
        memory_summary = self._generate_memory_summary(fused_memories)
        
        result = {
            "memories": fused_memories,
            "summary": memory_summary,
            "count": len(fused_memories),
            "types": {
                "semantic": len(semantic_memories),
                "context": len(context_memories),
                "emotional": len(emotional_memories)
            }
        }
        
        logger.info(f"🔍 记忆查询结果:")
        logger.info(f"   📊 总记忆数: {len(fused_memories)}")
        logger.info(f"   🧠 语义记忆: {len(semantic_memories)}")
        logger.info(f"   🪟 上下文记忆: {len(context_memories)}")
        logger.info(f"   😊 情感记忆: {len(emotional_memories)}")
        logger.info(f"   📝 记忆摘要: {memory_summary[:100]}...")
        
        return result
    
    def _query_semantic_memory(self, prompt: str, top_k: int) -> List[Dict[str, Any]]:
        """查询语义相似记忆"""
        if self.transformer is None:
            return []
        
        try:
            query_vector = self._embed_text(prompt)
            
            with self._db_lock:
                cursor = self.conn.cursor()
                cursor.execute("""
                    SELECT * FROM memory_records 
                    WHERE robot_id = ? AND vector IS NOT NULL
                    ORDER BY timestamp DESC
                    LIMIT 100
                """, (self.robot_id,))
                
                records = cursor.fetchall()
                if not records:
                    return []
            
            # 计算相似度
            similarities = []
            for record in records:
                try:
                    vector = json.loads(record["vector"])
                    similarity = self._cosine_similarity(query_vector, vector)
                    similarities.append((similarity, dict(record)))
                except Exception as e:
                    logger.warning(f"⚠️ 向量解析失败: {e}")
                    continue
            
            # 按相似度排序
            similarities.sort(key=lambda x: x[0], reverse=True)
            
            return [record for _, record in similarities[:top_k]]
            
        except Exception as e:
            logger.error(f"❌ 语义记忆查询失败: {e}")
            return []
    
    def _query_context_memory(self, session_id: str, top_k: int) -> List[Dict[str, Any]]:
        """查询上下文记忆"""
        with self._db_lock:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT * FROM memory_records 
                WHERE session_id = ? 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (session_id, top_k))
            
            return [dict(record) for record in cursor.fetchall()]
    
    def _query_emotional_memory(self, prompt: str, top_k: int) -> List[Dict[str, Any]]:
        """查询情感相关记忆"""
        # 简单的情感关键词匹配
        emotion_keywords = {
            "happy": ["开心", "高兴", "快乐", "兴奋", "愉快"],
            "sad": ["难过", "伤心", "悲伤", "沮丧", "失望"],
            "angry": ["生气", "愤怒", "恼火", "烦躁"],
            "surprised": ["惊讶", "震惊", "意外", "吃惊"],
            "excited": ["激动", "兴奋", "热情", "振奋"]
        }
        
        detected_emotions = []
        for emotion, keywords in emotion_keywords.items():
            for keyword in keywords:
                if keyword in prompt:
                    detected_emotions.append(emotion)
                    break
        
        if not detected_emotions:
            return []
        
        # 查询相关情感记忆
        with self._db_lock:
            cursor = self.conn.cursor()
            placeholders = ",".join(["?"] * len(detected_emotions))
            cursor.execute(f"""
                SELECT * FROM memory_records 
                WHERE robot_id = ? AND mood_tag IN ({placeholders})
                ORDER BY importance_score DESC, timestamp DESC 
                LIMIT ?
            """, (self.robot_id, *detected_emotions, top_k))
            
            return [dict(record) for record in cursor.fetchall()]
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """计算余弦相似度"""
        if len(vec1) != len(vec2):
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = sum(a * a for a in vec1) ** 0.5
        norm2 = sum(b * b for b in vec2) ** 0.5
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def _fuse_memories(
        self,
        semantic_memories: List[Dict[str, Any]],
        context_memories: List[Dict[str, Any]],
        emotional_memories: List[Dict[str, Any]],
        top_k: int
    ) -> List[Dict[str, Any]]:
        """融合不同类型的记忆"""
        all_memories = []
        
        # 添加语义记忆（权重1.0）
        for memory in semantic_memories:
            memory["weight"] = 1.0
            memory["source"] = "semantic"
            all_memories.append(memory)
        
        # 添加上下文记忆（权重1.2）
        for memory in context_memories:
            memory["weight"] = 1.2
            memory["source"] = "context"
            all_memories.append(memory)
        
        # 添加情感记忆（权重1.1）
        for memory in emotional_memories:
            memory["weight"] = 1.1
            memory["source"] = "emotional"
            all_memories.append(memory)
        
        # 去重并排序
        seen_ids = set()
        unique_memories = []
        
        for memory in all_memories:
            memory_id = memory["id"]
            if memory_id not in seen_ids:
                seen_ids.add(memory_id)
                unique_memories.append(memory)
        
        # 按权重和重要性排序
        unique_memories.sort(
            key=lambda x: x["weight"] * x.get("importance_score", 0.5),
            reverse=True
        )
        
        return unique_memories[:top_k]
    
    def _generate_memory_summary(self, memories: List[Dict[str, Any]]) -> str:
        """生成记忆摘要"""
        if not memories:
            return ""
        
        # 选择最重要的记忆
        important_memories = sorted(
            memories, 
            key=lambda x: x.get("importance_score", 0.5), 
            reverse=True
        )[:3]
        
        summary_parts = []
        for memory in important_memories:
            user_text = memory["user_text"]
            ai_response = memory["ai_response"]
            mood_tag = memory["mood_tag"]
            
            summary_parts.append(
                f"用户说'{user_text}'时，我回复'{ai_response}'，当时情绪是{mood_tag}"
            )
        
        return "。".join(summary_parts) + "。"
    
    def get_current_context(self, session_id: Optional[str] = None) -> str:
        """获取当前上下文"""
        if session_id is None:
            session_id = self.current_session_id
        
        if session_id is None:
            return ""
        
        context_window = self.context_windows.get(session_id)
        if context_window is None:
            return ""
        
        return context_window.current_context
    
    def get_recent_memories(self, session_id: str, limit: int = HISTORY_MAX_RECORDS) -> List[Dict[str, Any]]:
        """
        获取最近的记忆记录，用于构建历史对话
        
        Parameters
        ----------
        session_id : str
            会话ID
        limit : int
            获取的记录数量限制
            
        Returns
        -------
        List[Dict[str, Any]]
            最近的记忆记录列表
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 查询最近的记忆记录
                query = """
                SELECT user_text, ai_response, mood_tag, touch_zone, timestamp
                FROM memory_records 
                WHERE session_id = ? AND robot_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
                """
                
                cursor.execute(query, (session_id, self.robot_id, limit))
                rows = cursor.fetchall()
                
                # 转换为字典格式
                memories = []
                for row in rows:
                    memory = {
                        'user_text': row[0],
                        'ai_response': row[1],
                        'mood_tag': row[2],
                        'touch_zone': row[3],
                        'timestamp': row[4]
                    }
                    memories.append(memory)
                
                # 按时间顺序排列（最早的在前）
                memories.reverse()
                
                logger.info(f"📝 获取最近记忆: {len(memories)}条记录 (会话: {session_id})")
                return memories
                
        except Exception as e:
            logger.error(f"❌ 获取最近记忆失败: {e}")
            return []

    def get_memory_stats(self) -> Dict[str, Any]:
        """获取记忆统计信息"""
        with self._db_lock:
            cursor = self.conn.cursor()
            
            # 总记录数
            cursor.execute("SELECT COUNT(*) FROM memory_records WHERE robot_id = ?", (self.robot_id,))
            total_records = cursor.fetchone()[0]
            
            # 会话数
            cursor.execute("SELECT COUNT(*) FROM sessions WHERE robot_id = ?", (self.robot_id,))
            total_sessions = cursor.fetchone()[0]
            
            # 情绪分布
            cursor.execute("""
                SELECT mood_tag, COUNT(*) as count 
                FROM memory_records 
                WHERE robot_id = ? 
                GROUP BY mood_tag
            """, (self.robot_id,))
            emotion_distribution = dict(cursor.fetchall())
            
            # 重要性分布
            cursor.execute("""
                SELECT 
                    CASE 
                        WHEN importance_score >= 0.8 THEN 'high'
                        WHEN importance_score >= 0.5 THEN 'medium'
                        ELSE 'low'
                    END as importance_level,
                    COUNT(*) as count
                FROM memory_records 
                WHERE robot_id = ?
                GROUP BY importance_level
            """, (self.robot_id,))
            importance_distribution = dict(cursor.fetchall())
            
            return {
                "total_records": total_records,
                "total_sessions": total_sessions,
                "emotion_distribution": emotion_distribution,
                "importance_distribution": importance_distribution,
                "active_sessions": len(self.context_windows),
                "vector_dim": self.vector_dim
            }
    
    def clear_session_memory(self, session_id: Optional[str] = None) -> int:
        """清除会话记忆"""
        if session_id is None:
            session_id = self.current_session_id
        
        if session_id is None:
            return 0
        
        # 从内存中移除
        if session_id in self.context_windows:
            removed_count = len(self.context_windows[session_id].records)
            del self.context_windows[session_id]
        else:
            removed_count = 0
        
        # 从数据库中删除
        with self._db_lock:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM memory_records WHERE session_id = ?", (session_id,))
            cursor.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))
            self.conn.commit()
        
        logger.info(f"🗑️ 清除会话记忆: {session_id}, 删除记录数: {removed_count}")
        return removed_count
    
    def close(self):
        """关闭记忆系统"""
        with self._db_lock:
            if hasattr(self, 'conn'):
                self.conn.close()
        logger.info("🔒 增强记忆系统已关闭") 