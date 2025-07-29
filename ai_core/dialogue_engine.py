from typing import Optional

from .personality_engine import PersonalityEngine
from .semantic_memory import SemanticMemory


class DialogueEngine:
    """Dialogue system that grows with interactions.

    通过互动逐步成长的对话系统。
    """

    def __init__(self, personality: Optional[PersonalityEngine] = None, memory: Optional[SemanticMemory] = None):
        """Initialize dialogue engine with personality and memory modules.

        使用人格和记忆模块初始化对话引擎。
        """
        self.personality = personality or PersonalityEngine()
        self.memory = memory or SemanticMemory()
        self.stage = "cold_start"

    def generate_response(self, user_text: str, mood_tag: str = "neutral") -> str:
        """Generate an AI reply based on memory and personality.

        根据记忆和人格状态生成回答。
        """
        # update personality from mood_tag as behavior
        # 根据情绪标签更新人格
        self.personality.update(mood_tag)
        style = self.personality.get_personality_style()
        past = self.memory.query_memory(user_text)
        past_summary = " ".join([p["ai_response"] for p in past])
        # Placeholder: real system would invoke LLM here
        # 示例实现：真实系统会调用大型语言模型
        response = f"[{style}] I remember: {past_summary} | You said: {user_text}"
        self.memory.add_memory(user_text, response, mood_tag)
        return response
