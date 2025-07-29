import datetime
from typing import List, Dict, Any

import numpy as np

try:
    import faiss  # type: ignore
except ImportError:  # pragma: no cover
    faiss = None


class SemanticMemory:
    """Simple vector-based semantic memory using FAISS if available.

    基于向量的语义记忆模块，如有 FAISS 库则使用其加速搜索。
    """

    def __init__(self, vector_dim: int = 384):
        """Initialize memory store and optional FAISS index.

        初始化记忆存储及 FAISS 索引（如果可用）。
        """
        self.vector_dim = vector_dim
        self.records: List[Dict[str, Any]] = []
        if faiss is not None:
            self.index = faiss.IndexFlatL2(vector_dim)
        else:
            self.index = None

    def _embed(self, text: str) -> np.ndarray:
        """Convert text to embedding vector. Placeholder implementation.

        将文本转换为向量，示例实现。
        """
        np.random.seed(abs(hash(text)) % (2**32))
        return np.random.rand(self.vector_dim).astype('float32')

    def add_memory(self, user_text: str, ai_response: str, mood_tag: str) -> None:
        """Add a conversation record into memory.

        新增一条对话记录到记忆库中。
        """
        vec = self._embed(user_text)
        record = {
            "time": datetime.datetime.utcnow(),
            "user_text": user_text,
            "ai_response": ai_response,
            "mood_tag": mood_tag,
            "topic_vector": vec,
        }
        self.records.append(record)
        if self.index is not None:
            self.index.add(np.expand_dims(vec, 0))

    def query_memory(self, prompt: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Return most relevant past interactions for the prompt.

        根据提示查询最相关的历史对话。
        """
        query_vec = self._embed(prompt)
        if self.index is not None and len(self.records) > 0:
            distances, indices = self.index.search(np.expand_dims(query_vec, 0), top_k)
            result = [self.records[i] for i in indices[0] if i < len(self.records)]
            return result
        # fallback linear search
        # 回退到线性搜索
        scores = [float(np.dot(r["topic_vector"], query_vec)) for r in self.records]
        top_indices = np.argsort(scores)[-top_k:][::-1]
        return [self.records[i] for i in top_indices]
