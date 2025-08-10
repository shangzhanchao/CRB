"""Hybrid memory system combining session memory and semantic memory.

融合记忆系统，结合会话记录和语义记忆，提供更智能的记忆管理。
"""

import datetime
import logging
import json
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional, Tuple
from collections import deque

from .semantic_memory import SemanticMemory
from .constants import (
    SESSION_MEMORY_LIMIT,
    MEMORY_FUSION_THRESHOLD,
    CONTEXT_WINDOW_SIZE,
    ROBOT_MEMORY_PREFIX,
    MEMORY_CONFIG,
    LOG_LEVEL,
)

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)


@dataclass
class SessionRecord:
    """会话记录数据结构"""
    robot_id: str                    # 机器人编号
    timestamp: datetime.datetime      # 时间戳
    user_text: str                   # 用户输入
    ai_response: str                 # AI回复
    mood_tag: str                    # 情绪标签
    touch_zone: Optional[int]        # 触摸区域
    context_id: str                  # 上下文ID
    importance_score: float           # 重要性评分


@dataclass
class SemanticRecord:
    """语义记忆数据结构"""
    robot_id: str                    # 机器人编号
    timestamp: datetime.datetime      # 时间戳
    content: str                     # 记忆内容
    vector: List[float]              # 语义向量
    mood_tag: str                    # 情绪标签
    touch_zone: Optional[int]        # 触摸区域
    importance_score: float           # 重要性评分
    memory_type: str                 # 记忆类型


class HybridMemoryManager:
    """融合记忆管理器
    
    结合会话记录（短期记忆）和语义记忆（长期记忆）的智能记忆系统。
    """

    def __init__(
        self,
        robot_id: str,
        session_limit: int = SESSION_MEMORY_LIMIT,
        semantic_memory: Optional[SemanticMemory] = None,
    ):
        """初始化融合记忆管理器
        
        Parameters
        ----------
        robot_id: str
            机器人编号
        session_limit: int, optional
            会话记录最大条数，默认为 SESSION_MEMORY_LIMIT
        semantic_memory: SemanticMemory, optional
            语义记忆实例，如果为None则创建新的实例
        """
        self.robot_id = robot_id
        self.session_limit = session_limit
        self.session_memory = deque(maxlen=session_limit)  # 使用deque实现FIFO
        self.semantic_memory = semantic_memory or SemanticMemory()
        self.context_counter = 0
        
        logger.info(f"🔧 初始化融合记忆管理器 - 机器人ID: {robot_id}")
        logger.info(f"   📊 会话记录限制: {session_limit}")
        logger.info(f"   🧠 语义记忆状态: {'已连接' if semantic_memory else '新建'}")
    
    def add_memory(
        self,
        user_text: str,
        ai_response: str,
        mood_tag: str = "neutral",
        user_id: str = "unknown",
        touched: bool = False,
        touch_zone: Optional[int] = None,
    ) -> None:
        """添加记忆到两个层次
        
        Parameters
        ----------
        user_text: str
            用户输入文本
        ai_response: str
            AI回复文本
        mood_tag: str, optional
            情绪标签，默认为 "neutral"
        user_id: str, optional
            用户ID，默认为 "unknown"
        touched: bool, optional
            是否被触摸，默认为 False
        touch_zone: int | None, optional
            触摸区域，默认为 None
        """
        # 生成上下文ID
        self.context_counter += 1
        context_id = f"{self.robot_id}_ctx_{self.context_counter}"
        
        # 计算重要性评分
        importance_score = self._calculate_importance_score(
            user_text, ai_response, mood_tag, touched
        )
        
        # 1. 添加到会话记录
        session_record = SessionRecord(
            robot_id=self.robot_id,
            timestamp=datetime.datetime.utcnow(),
            user_text=user_text,
            ai_response=ai_response,
            mood_tag=mood_tag,
            touch_zone=touch_zone,
            context_id=context_id,
            importance_score=importance_score,
        )
        
        self.session_memory.append(session_record)
        
        # 2. 添加到语义记忆
        self.semantic_memory.add_memory(
            user_text=user_text,
            ai_response=ai_response,
            mood_tag=mood_tag,
            user_id=user_id,
            touched=touched,
            touch_zone=touch_zone,
        )
        
        logger.info(f"💾 记忆已添加 - 上下文ID: {context_id}")
        logger.info(f"   📝 用户: {user_text}")
        logger.info(f"   🤖 AI: {ai_response}")
        logger.info(f"   😊 情绪: {mood_tag}")
        logger.info(f"   📊 重要性: {importance_score:.3f}")
        logger.info(f"   📈 会话记录数: {len(self.session_memory)}")
    
    def query_memory(
        self,
        prompt: str,
        top_k: int = 5,
        user_id: Optional[str] = None,
        use_fusion: bool = True,
    ) -> Dict[str, Any]:
        """融合查询两个层次的记忆
        
        Parameters
        ----------
        prompt: str
            查询提示
        top_k: int, optional
            返回记录数量，默认为 5
        user_id: str | None, optional
            用户ID过滤，默认为 None
        use_fusion: bool, optional
            是否使用融合查询，默认为 True
        
        Returns
        -------
        Dict[str, Any]
            包含记忆查询结果的字典
        """
        logger.info(f"🔍 开始记忆查询 - 提示: {prompt}")
        
        # 1. 查询会话记录
        session_results = self._query_session_memory(prompt, top_k)
        
        # 2. 查询语义记忆
        semantic_results = self.semantic_memory.query_memory(
            prompt, top_k=top_k, user_id=user_id
        )
        
        # 3. 融合结果
        if use_fusion and session_results and semantic_results:
            fused_results = self._fuse_memories(
                session_results, semantic_results, top_k
            )
            memory_type = "fused"
        else:
            # 优先使用会话记录，如果为空则使用语义记忆
            if session_results:
                fused_results = session_results
                memory_type = "session"
            else:
                fused_results = semantic_results
                memory_type = "semantic"
        
        # 4. 生成记忆摘要
        memory_summary = self._generate_memory_summary(fused_results)
        
        result = {
            "memory_type": memory_type,
            "records": fused_results,
            "summary": memory_summary,
            "session_count": len(session_results),
            "semantic_count": len(semantic_results),
            "total_count": len(fused_results),
        }
        
        logger.info(f"📋 记忆查询完成")
        logger.info(f"   🎯 记忆类型: {memory_type}")
        logger.info(f"   📊 会话记录: {len(session_results)}")
        logger.info(f"   🧠 语义记忆: {len(semantic_results)}")
        logger.info(f"   📝 总记录数: {len(fused_results)}")
        
        return result
    
    def get_context_memory(
        self, window_size: int = CONTEXT_WINDOW_SIZE
    ) -> List[SessionRecord]:
        """获取最近的上下文记忆
        
        Parameters
        ----------
        window_size: int, optional
            上下文窗口大小，默认为 CONTEXT_WINDOW_SIZE
        
        Returns
        -------
        List[SessionRecord]
            最近的会话记录列表
        """
        if not self.session_memory:
            return []
        
        # 获取最近的记录
        recent_records = list(self.session_memory)[-window_size:]
        
        logger.info(f"📖 获取上下文记忆 - 窗口大小: {window_size}")
        logger.info(f"   📊 返回记录数: {len(recent_records)}")
        
        return recent_records
    
    def archive_important_memories(self, importance_threshold: float = 0.8) -> int:
        """将重要记忆归档到语义记忆
        
        Parameters
        ----------
        importance_threshold: float, optional
            重要性阈值，默认为 0.8
        
        Returns
        -------
        int
            归档的记忆数量
        """
        if not self.session_memory:
            return 0
        
        archived_count = 0
        records_to_remove = []
        
        for record in self.session_memory:
            if record.importance_score >= importance_threshold:
                # 将重要记忆转换为语义记忆格式
                semantic_record = SemanticRecord(
                    robot_id=record.robot_id,
                    timestamp=record.timestamp,
                    content=f"用户: {record.user_text} | AI: {record.ai_response}",
                    vector=self.semantic_memory._embed(record.user_text),
                    mood_tag=record.mood_tag,
                    touch_zone=record.touch_zone,
                    importance_score=record.importance_score,
                    memory_type="archived_session",
                )
                
                # 添加到语义记忆（这里需要扩展语义记忆的接口）
                records_to_remove.append(record)
                archived_count += 1
        
        # 从会话记忆中移除已归档的记录
        for record in records_to_remove:
            try:
                self.session_memory.remove(record)
            except ValueError:
                pass  # 记录可能已经被移除
        
        logger.info(f"📦 记忆归档完成")
        logger.info(f"   📊 归档数量: {archived_count}")
        logger.info(f"   📈 剩余会话记录: {len(self.session_memory)}")
        
        return archived_count
    
    def _query_session_memory(
        self, prompt: str, top_k: int
    ) -> List[Dict[str, Any]]:
        """查询会话记忆
        
        Parameters
        ----------
        prompt: str
            查询提示
        top_k: int
            返回记录数量
        
        Returns
        -------
        List[Dict[str, Any]]
            会话记忆记录列表
        """
        if not self.session_memory:
            return []
        
        # 简单的关键词匹配（可以后续优化为向量搜索）
        prompt_lower = prompt.lower()
        matched_records = []
        
        for record in self.session_memory:
            # 检查用户输入和AI回复中是否包含关键词
            user_match = any(word in record.user_text.lower() 
                           for word in prompt_lower.split())
            ai_match = any(word in record.ai_response.lower() 
                          for word in prompt_lower.split())
            
            if user_match or ai_match:
                matched_records.append({
                    "time": record.timestamp,
                    "user_text": record.user_text,
                    "ai_response": record.ai_response,
                    "mood_tag": record.mood_tag,
                    "user_id": self.robot_id,
                    "touched": False,  # 会话记录中不直接存储触摸状态
                    "touch_zone": record.touch_zone,
                    "topic_vector": [],  # 会话记录不存储向量
                    "importance_score": record.importance_score,
                    "memory_type": "session",
                })
        
        # 按重要性评分和时间排序
        matched_records.sort(
            key=lambda x: (x["importance_score"], x["time"]), 
            reverse=True
        )
        
        return matched_records[:top_k]
    
    def _fuse_memories(
        self,
        session_memories: List[Dict[str, Any]],
        semantic_memories: List[Dict[str, Any]],
        top_k: int,
    ) -> List[Dict[str, Any]]:
        """融合会话记忆和语义记忆
        
        Parameters
        ----------
        session_memories: List[Dict[str, Any]]
            会话记忆列表
        semantic_memories: List[Dict[str, Any]]
            语义记忆列表
        top_k: int
            返回记录数量
        
        Returns
        -------
        List[Dict[str, Any]]
            融合后的记忆列表
        """
        # 合并所有记忆
        all_memories = session_memories + semantic_memories
        
        # 去重处理（基于内容和时间）
        unique_memories = []
        seen_contents = set()
        
        for memory in all_memories:
            content_key = f"{memory['user_text']}_{memory['ai_response']}"
            if content_key not in seen_contents:
                seen_contents.add(content_key)
                unique_memories.append(memory)
        
        # 按时间排序（最新的在前）
        unique_memories.sort(key=lambda x: x["time"], reverse=True)
        
        # 计算相似度并去重
        final_memories = []
        for memory in unique_memories:
            is_similar = False
            for existing in final_memories:
                similarity = self._calculate_similarity(memory, existing)
                if similarity > MEMORY_FUSION_THRESHOLD:
                    is_similar = True
                    break
            
            if not is_similar:
                final_memories.append(memory)
                if len(final_memories) >= top_k:
                    break
        
        return final_memories
    
    def _calculate_similarity(
        self, memory1: Dict[str, Any], memory2: Dict[str, Any]
    ) -> float:
        """计算两个记忆的相似度
        
        Parameters
        ----------
        memory1: Dict[str, Any]
            第一个记忆
        memory2: Dict[str, Any]
            第二个记忆
        
        Returns
        -------
        float
            相似度分数（0-1）
        """
        # 简单的文本相似度计算
        text1 = f"{memory1['user_text']} {memory1['ai_response']}".lower()
        text2 = f"{memory2['user_text']} {memory2['ai_response']}".lower()
        
        # 计算词汇重叠度
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    def _calculate_importance_score(
        self,
        user_text: str,
        ai_response: str,
        mood_tag: str,
        touched: bool,
    ) -> float:
        """计算记忆的重要性评分
        
        Parameters
        ----------
        user_text: str
            用户输入
        ai_response: str
            AI回复
        mood_tag: str
            情绪标签
        touched: bool
            是否被触摸
        
        Returns
        -------
        float
            重要性评分（0-1）
        """
        score = 0.5  # 基础分数
        
        # 1. 情绪强度
        emotion_scores = {
            "happy": 0.8,
            "excited": 0.9,
            "angry": 0.7,
            "sad": 0.6,
            "surprised": 0.8,
            "neutral": 0.5,
        }
        score += emotion_scores.get(mood_tag, 0.5) * 0.3
        
        # 2. 触摸交互
        if touched:
            score += 0.2
        
        # 3. 文本长度（更长的对话可能更重要）
        text_length = len(user_text) + len(ai_response)
        score += min(text_length / 1000, 0.2)  # 最多加0.2分
        
        # 4. 特殊关键词
        important_keywords = ["喜欢", "讨厌", "重要", "记住", "love", "hate", "important"]
        for keyword in important_keywords:
            if keyword in user_text.lower() or keyword in ai_response.lower():
                score += 0.1
                break
        
        return min(score, 1.0)  # 确保不超过1.0
    
    def _generate_memory_summary(
        self, memories: List[Dict[str, Any]]
    ) -> str:
        """生成记忆摘要
        
        Parameters
        ----------
        memories: List[Dict[str, Any]]
            记忆列表
        
        Returns
        -------
        str
            记忆摘要
        """
        if not memories:
            return ""
        
        summary_parts = []
        
        # 选择最重要的记忆生成摘要
        important_memories = sorted(
            memories, 
            key=lambda x: x.get("importance_score", 0), 
            reverse=True
        )[:3]
        
        for i, memory in enumerate(important_memories):
            user_text = memory["user_text"]
            ai_response = memory["ai_response"]
            mood = memory.get("mood_tag", "neutral")
            
            summary_part = f"用户说'{user_text}'时，我回复'{ai_response}'"
            if mood != "neutral":
                summary_part += f"，当时情绪是{mood}"
            
            summary_parts.append(summary_part)
        
        return "。".join(summary_parts)
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """获取记忆统计信息
        
        Returns
        -------
        Dict[str, Any]
            记忆统计信息
        """
        return {
            "robot_id": self.robot_id,
            "session_count": len(self.session_memory),
            "session_limit": self.session_limit,
            "context_counter": self.context_counter,
            "semantic_memory_available": self.semantic_memory is not None,
        }
    
    def clear_session_memory(self) -> int:
        """清空会话记忆
        
        Returns
        -------
        int
            清除的记录数量
        """
        count = len(self.session_memory)
        self.session_memory.clear()
        self.context_counter = 0
        
        logger.info(f"🗑️ 会话记忆已清空 - 清除记录数: {count}")
        
        return count 