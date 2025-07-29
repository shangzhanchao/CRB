"""AI Companion Robot core modules.

AI陪伴机器人核心模块。

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
from .dialogue_engine import DialogueEngine
from .intelligent_core import IntelligentCore, UserInput
from . import global_state
from .global_state import increment, reset

__all__ = [
    "PersonalityEngine",
    "SemanticMemory",
    "EmotionPerception",
    "EmotionState",
    "DEFAULT_AUDIO_PATH",
    "DEFAULT_IMAGE_PATH",
    "DialogueEngine",
    "IntelligentCore",
    "UserInput",
    "increment",
    "reset",
    "global_state",
]
