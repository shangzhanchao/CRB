"""Dialogue generation module.

文件结构：

```
DialogueEngine -> 负责根据人格与记忆生成回复
```
"""

from typing import Optional

from .personality_engine import PersonalityEngine
from .semantic_memory import SemanticMemory


class DialogueEngine:
    """Dialogue system that grows with interactions.

    通过互动逐步成长的对话系统。
    """

    def __init__(
        self,
        personality: Optional[PersonalityEngine] = None,
        memory: Optional[SemanticMemory] = None,
        cold_start_threshold: int = 3,
        active_threshold: int = 6,
    ) -> None:
        """Initialize dialogue engine with personality and memory modules.

        使用人格和记忆模块初始化对话引擎。

        Parameters
        ----------
        personality: PersonalityEngine, optional
            Custom personality engine. 默认为 :class:`PersonalityEngine` 实例。
        memory: SemanticMemory, optional
            Memory storage module. 默认为 :class:`SemanticMemory`。
        cold_start_threshold: int, optional
            Number of interactions before switching from cold start to
            learning stage.  冷启动阶段持续的交互次数，默认 3。
        active_threshold: int, optional
            Number of interactions before switching from learning to active
            stage.  学习阶段持续的交互次数，默认 6。
        """
        self.personality = personality or PersonalityEngine()
        self.memory = memory or SemanticMemory()
        self.stage = "cold_start"            # 当前对话阶段
        self.counter = 0                      # 交互计数器
        self.cold_start_threshold = cold_start_threshold  # 冷启动阈值
        self.active_threshold = active_threshold          # 主动阶段阈值

    def generate_response(self, user_text: str, mood_tag: str = "neutral") -> str:
        """Generate an AI reply based on memory and personality.

        根据记忆和人格状态生成回答。

        Parameters
        ----------
        user_text: str
            Incoming user message.
        mood_tag: str, optional
            Emotion label influencing personality update. Defaults to
            ``"neutral"``.
        """
        # update personality from mood_tag as behavior
        # 根据情绪标签更新人格
        self.personality.update(mood_tag)
        self.counter += 1
        if self.stage == "cold_start" and self.counter >= self.cold_start_threshold:
            self.stage = "learning"  # 进入学习阶段
        if self.stage == "learning" and self.counter >= self.active_threshold:
            self.stage = "active"    # 进入主动阶段

        style = self.personality.get_personality_style()
        past = self.memory.query_memory(user_text)
        past_summary = " ".join([p["ai_response"] for p in past])  # 简单拼接历史回复

        if self.stage == "cold_start":
            response = f"[{style}] You said: {user_text}"
        elif self.stage == "learning":
            response = (
                f"[{style}] I remember: {past_summary} | You said: {user_text}. "
                "Could you tell me more?"
            )
        else:
            response = f"[{style}] Based on our chats: {past_summary} | {user_text}"

        self.memory.add_memory(user_text, response, mood_tag)  # 记录本次对话
        return response
