"""Dialogue generation module.

文件结构:

```
DialogueEngine -> 负责根据人格与记忆生成回复
```

The engine receives perceived emotion, user identity and textual input from
``IntelligentCore``. It consults the personality vector and semantic memory to
compose a reply, then maps mood and touch into actions and expressions.
该模块从 ``IntelligentCore`` 获取情绪、身份和文本信息，结合人格向量与
语义记忆生成回复，并给出相应的动作和表情。
"""

# Growth stages
# 成长阶段说明:
# 1. sprout   - 萌芽期 (0~3 天)
# 2. enlighten - 启蒙期 (3~10 天)
# 3. resonate - 共鸣期 (10~30 天)
# 4. awaken   - 觉醒期 (30 天以上)

from dataclasses import dataclass
from typing import Optional

from . import global_state

from .personality_engine import PersonalityEngine
from .semantic_memory import SemanticMemory
from .service_clients import call_llm, call_tts


@dataclass
class DialogueResponse:
    """Structured output of the dialogue engine.

    对话引擎生成的结构化回应，包括文本、语音风格、动作和表情。
    """

    text: str
    voice: str
    action: str
    expression: str
    audio: str = ""


class DialogueEngine:
    """Dialogue system that grows with interactions.

    通过互动逐步成长的对话系统。
    """

    def __init__(
        self,
        personality: Optional[PersonalityEngine] = None,
        memory: Optional[SemanticMemory] = None,
        llm_url: str | None = None,
        tts_url: str | None = None,
    ) -> None:
        """Initialize dialogue engine with personality and memory modules.

        使用人格和记忆模块初始化对话引擎。

        Parameters
        ----------
        personality: PersonalityEngine, optional
            Custom personality engine. 默认为 :class:`PersonalityEngine` 实例。
        memory: SemanticMemory, optional
            Memory storage module. 默认为 :class:`SemanticMemory`。
        llm_url: str | None, optional
            Endpoint for remote large language model service. If ``None``,
            simple local templates are used.
        tts_url: str | None, optional
            Endpoint for text-to-speech service. ``None`` disables TTS.
        """
        self.personality = personality or PersonalityEngine()
        self.memory = memory or SemanticMemory()
        self.llm_url = llm_url
        self.tts_url = tts_url
        self.stage = global_state.get_growth_stage()  # 初始成长阶段

    def generate_response(
        self,
        user_text: str,
        mood_tag: str = "neutral",
        user_id: str = "unknown",
        touched: bool = False,
    ) -> DialogueResponse:
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
        # 1. personality update
        # 根据情绪标签与触摸行为更新人格向量
        self.personality.update(mood_tag)
        if touched:
            self.personality.update("touch")
        # 2. determine growth stage using global metrics
        # 根据全局统计信息判断成长阶段
        self.stage = global_state.get_growth_stage()

        style = self.personality.get_personality_style()
        past = self.memory.query_memory(user_text, user_id=user_id)
        # 从记忆中取得相关历史回答并简要拼接
        past_summary = " ".join([p["ai_response"] for p in past])

        # 3. generate base response according to growth stage
        if self.stage == "sprout":
            # 萌芽期只会发出简单的咿呀声
            response = "呀呀" if user_text else "咿呀"
        elif self.stage == "enlighten":
            # 启蒙期模仿问候词
            if any(k in user_text for k in ("你好", "hi", "早安")):
                response = user_text
            else:
                response = "你好"
        elif self.stage == "resonate":
            # 共鸣期可以进行简短交流
            response = f"[{style}] {user_text}? 我在听哦"
        else:  # awaken
            # 觉醒期结合历史记忆给出丰富回复
            response = f"[{style}] Based on our chats: {past_summary} | {user_text}"

        # 可选：调用远程大模型优化回复
        if self.llm_url:
            llm_out = call_llm(response, self.llm_url)
            if llm_out:
                response = llm_out

        # 4. store this interaction in memory
        self.memory.add_memory(user_text, response, mood_tag, user_id, touched)

        # 5. derive action and expression from mood and touch
        expression = {
            "happy": "smile",
            "angry": "frown",
            "calm": "neutral",
        }.get(mood_tag, "neutral")

        action = "hug" if touched else "idle"

        # TTS generates an audio URL when service is provided
        audio_url = call_tts(response, self.tts_url) if self.tts_url else ""

        return DialogueResponse(
            text=response,
            voice=style,
            action=action,
            expression=expression,
            audio=audio_url,
        )
