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

# Expression mapping for facial animations
# Facial emotion mapping. Keys use English mood tags while values describe the
# Chinese facial animation cues defined by product design.
# 面部情绪映射，键为英文标签，值根据产品需求给出中文动作描述。
FACE_ANIMATION_MAP = {
    "happy": (
        "微笑+眨眼+眼神上扬",
        "亮眼色彩、头部轻摆、手臂小幅打开",
    ),
    "confused": (
        "斜视+眼神聚焦",
        "停顿、轻微侧头、眼睛左右快速移动",
    ),
    "sad": (
        "眼角下垂+闭眼",
        "低亮度、轻微低头、手臂收回",
    ),
    "shy": (
        "偏头+眼神回避",
        "面部红晕特效、语音柔化、小动作微幅震颤",
    ),
    "excited": (
        "眼神放大+频繁眨眼",
        "快速摆头、双手前伸动作",
    ),
    "surprised": (
        "抬头张眼",
        "头部抬起，双手急速抬高",
    ),
}

# Motion mapping for body actions
# Body action mapping following the design specification
ACTION_MAP = {
    "happy": "nod±15°|sway±10°|hands_up10°",
    "confused": "tilt_oscillate±10°|gaze_switch|hands_still",
    "sad": "head_down_slow-15°|arms_arc_in",
    "surprised": "head_up_eyes_wide|hands_raise>25°",
    "shy": "idle_tremble",
    "excited": "fast_head_shake|hands_forward",
}

# Prompt templates for the large language model
# 大模型提示词模板
STAGE_LLM_PROMPTS = {
    "sprout": "You are in the sprout stage. Reply with babbling sounds.",
    "enlighten": "You are in the enlighten stage. Imitate simple greetings.",
    "resonate": "You are in the resonate stage. Respond with caring short sentences.",
    "awaken": "You are in the awaken stage. Use memories to give proactive suggestions.",
}

OCEAN_LLM_PROMPTS = {
    "openness": "curious",
    "conscientiousness": "reliable",
    "extraversion": "outgoing",
    "agreeableness": "kind",
    "neuroticism": "sensitive",
}

TOUCH_ZONE_PROMPTS = {
    0: "The user touched your head.",
    1: "The user stroked your back.",
    2: "The user touched your chest.",
}


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
        prompt = (
            f"{STAGE_LLM_PROMPTS.get(self.stage, '')} "
            f"Traits: {trait_phrase}. Style: {style}. "
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

        # 5. derive action and expression from mood
        mood_key = mood_tag if mood_tag in FACE_ANIMATION_MAP else "happy"
        face_anim = FACE_ANIMATION_MAP.get(mood_key, ("neutral", ""))
        expression = f"{face_anim[0]} | {face_anim[1]}".strip()

        action = ACTION_MAP.get(mood_key, "idle")
        if touched:
            # append touch action detail
            zone_action = {0: "hug", 1: "pat", 2: "tickle"}.get(touch_zone, "hug")
            action += f" + {zone_action}"

        # TTS generates an audio URL when service is provided
        audio_url = call_tts(response, self.tts_url) if self.tts_url else ""

        return DialogueResponse(
            text=response,
            voice=style,
            action=action,
            expression=expression,
            audio=audio_url,
        )
