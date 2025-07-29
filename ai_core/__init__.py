"""Companion Robot Intelligent Brain core modules.

陪伴机器人智能大脑核心模块。

Structure overview:

```
personality_engine -> OCEAN人格引擎
semantic_memory    -> 语义记忆系统
emotion_perception -> 情绪识别模块
dialogue_engine    -> 对话生成
intelligent_core   -> 模块调度器
```
"""

from .personality_engine import PersonalityEngine
from .semantic_memory import SemanticMemory
from .emotion_perception import (
    EmotionPerception,
    EmotionState,
    DEFAULT_AUDIO_PATH,
    DEFAULT_IMAGE_PATH,
)
from .dialogue_engine import DialogueEngine, DialogueResponse
from .intelligent_core import IntelligentCore, UserInput
from .service_clients import (
    call_asr,
    call_tts,
    call_llm,
    call_voiceprint,
    DEFAULT_TTS_URL,
    DEFAULT_ASR_URL,
    DEFAULT_LLM_URL,
    DEFAULT_VOICEPRINT_URL,
)
from . import global_state
from .global_state import (
    increment,
    reset,
    get_growth_stage,
    add_audio_duration,
    days_since_start,
    AUDIO_DATA_SECONDS,
)

__all__ = [
    "PersonalityEngine",
    "SemanticMemory",
    "EmotionPerception",
    "EmotionState",
    "DEFAULT_AUDIO_PATH",
    "DEFAULT_IMAGE_PATH",
    "DialogueEngine",
    "DialogueResponse",
    "IntelligentCore",
    "UserInput",
    "call_asr",
    "call_tts",
    "call_llm",
    "call_voiceprint",
    "DEFAULT_TTS_URL",
    "DEFAULT_ASR_URL",
    "DEFAULT_LLM_URL",
    "DEFAULT_VOICEPRINT_URL",
    "increment",
    "reset",
    "get_growth_stage",
    "add_audio_duration",
    "days_since_start",
    "AUDIO_DATA_SECONDS",
    "global_state",
]
