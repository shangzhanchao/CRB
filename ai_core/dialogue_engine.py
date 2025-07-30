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
import logging

from . import global_state

from .personality_engine import PersonalityEngine
from .semantic_memory import SemanticMemory
from .service_clients import call_llm, call_tts
from .constants import (
    DEFAULT_GROWTH_STAGE,
    LOG_LEVEL,
    FACE_ANIMATION_MAP,
    ACTION_MAP,
    STAGE_LLM_PROMPTS,
    STAGE_LLM_PROMPTS_CN,
    OCEAN_LLM_PROMPTS,
    OCEAN_LLM_PROMPTS_CN,
    TOUCH_ZONE_PROMPTS,
)

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)



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
        if not self.stage:
            self.stage = DEFAULT_GROWTH_STAGE
        logger.debug("Dialogue engine initialized at stage %s", self.stage)

    def generate_response(
        self,
        user_text: str,
        mood_tag: str = "neutral",
        user_id: str = "unknown",
        touched: bool = False,
        touch_zone: int | None = None,
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
        touched: bool, optional
            Whether the robot was touched during this interaction.
        touch_zone: int | None, optional
            Identifier for the touch sensor zone. ``None`` means no touch
            detected.
        """
        logger.info(
            "Generating response for user %s with mood %s", user_id, mood_tag
        )
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
        logger.debug("Retrieved %d past records", len(past))
        # 从记忆中取得相关历史回答并简要拼接
        past_summary = " ".join([p["ai_response"] for p in past])

        # 3. generate base response
        if self.stage == "sprout":
            base_resp = "呀呀" if user_text else "咿呀"
        elif self.stage == "enlighten":
            base_resp = "你好" if user_text else "你好"
        elif self.stage == "resonate":
            base_resp = f"[{style}] {user_text}? 我在听哦"
        else:  # awaken
            base_resp = f"[{style}] Based on our chats: {past_summary} | {user_text}"

        # Construct LLM prompt combining stage, personality and touch info
        touch_phrase = TOUCH_ZONE_PROMPTS.get(touch_zone, "") if touched else ""
        trait_phrase = ", ".join(OCEAN_LLM_PROMPTS.values())
        trait_phrase_cn = "、".join(OCEAN_LLM_PROMPTS_CN.values())
        stage_phrase = STAGE_LLM_PROMPTS.get(self.stage, "")
        stage_phrase_cn = STAGE_LLM_PROMPTS_CN.get(self.stage, "")
        prompt = (
            f"{stage_phrase} {stage_phrase_cn} "
            f"Traits: {trait_phrase} ({trait_phrase_cn}). Style: {style}. "
            f"{touch_phrase} Past: {past_summary}. User: {user_text}"
        )

        response = base_resp
        if self.llm_url:
            llm_out = call_llm(prompt, self.llm_url)
            if llm_out:
                response = llm_out

        # 4. store this interaction in memory
        self.memory.add_memory(
            user_text,
            response,
            mood_tag,
            user_id,
            touched,
            touch_zone,
        )
        logger.debug("Memory stored for user %s", user_id)

        # 5. derive action and expression from mood
        mood_key = mood_tag if mood_tag in FACE_ANIMATION_MAP else "happy"
        face_anim = FACE_ANIMATION_MAP.get(mood_key, ("neutral", ""))
        expression = f"{face_anim[0]} | {face_anim[1]}".strip()

        action = ACTION_MAP.get(mood_key, "idle")
        if touched:
            # append touch action detail
            zone_action = {0: "hug", 1: "pat", 2: "tickle"}.get(touch_zone, "hug")
            action += f" + {zone_action}"
        logger.debug("Action: %s | Expression: %s", action, expression)

        # TTS generates an audio URL when service is provided
        audio_url = call_tts(response, self.tts_url) if self.tts_url else ""
        if not audio_url:
            audio_url = "n/a"  # 保证音频字段不为空

        logger.info("Generated response: %s", response)

        return DialogueResponse(
            text=response,
            voice=style,
            action=action,
            expression=expression,
            audio=audio_url,
        )
