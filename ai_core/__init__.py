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
from .emotion_perception import EmotionPerception, EmotionState
from .dialogue_engine import DialogueEngine, DialogueResponse
from .intelligent_core import IntelligentCore, UserInput
# Service API wrappers 服务接口封装
from .service_api import (
    call_asr,
    call_tts,
    call_llm,
    call_voiceprint,
    call_memory_save,
    call_memory_query,
)
# Constants shared across modules. 统一的默认常量
from .constants import (
    DEFAULT_TTS_URL,  # 默认 TTS 服务地址
    DEFAULT_ASR_URL,  # 默认 ASR 服务地址
    DEFAULT_LLM_URL,  # 默认大模型服务地址
    DEFAULT_VOICEPRINT_URL,  # 默认声纹识别服务地址
    DEFAULT_AUDIO_PATH,  # 演示音频文件
    DEFAULT_IMAGE_PATH,  # 演示图像文件
    DEFAULT_GROWTH_STAGE,  # 默认成长阶段
    DEFAULT_PERSONALITY_VECTOR,  # 默认人格向量
    EMOTION_STATES,  # 情绪状态列表
    EMOTION_PROMPT_TEMPLATE,  # 情绪识别提示模板
    DEFAULT_MEMORY_SAVE_URL,  # 记忆存储服务地址
    DEFAULT_MEMORY_QUERY_URL,  # 记忆查询服务地址
    MULTI_MODAL_EMOTION_PROMPT,  # 多模态情绪识别提示模板
)
# Global metrics utilities 全局统计相关工具
from . import global_state
from .global_state import (
    increment,  # 递增交互计数
    reset,  # 重置全局状态
    get_growth_stage,  # 获取成长阶段
    add_audio_duration,  # 累加语音数据时长
    days_since_start,  # 获取启动以来的天数
    AUDIO_DATA_SECONDS,  # 当前累计语音时长
)

# Re-export commonly used symbols for convenience 便于外部使用

__all__ = [
    "PersonalityEngine",      # 人格成长引擎
    "SemanticMemory",        # 语义记忆系统
    "EmotionPerception",     # 情绪识别模块
    "EmotionState",          # 情绪状态数据类
    "DEFAULT_AUDIO_PATH",    # 默认音频路径
    "DEFAULT_IMAGE_PATH",    # 默认图像路径
    "DialogueEngine",        # 对话生成引擎
    "DialogueResponse",      # 对话输出结构
    "IntelligentCore",       # 系统调度核心
    "UserInput",             # 用户输入数据类
    "call_asr",              # 调用语音识别服务
    "call_tts",              # 调用语音合成服务
    "call_llm",              # 调用大模型服务
    "call_voiceprint",       # 调用声纹识别服务
    "call_memory_save",      # 调用记忆存储服务
    "call_memory_query",     # 调用记忆查询服务
    "DEFAULT_TTS_URL",       # TTS 服务默认地址
    "DEFAULT_ASR_URL",       # ASR 服务默认地址
    "DEFAULT_LLM_URL",       # LLM 服务默认地址
    "DEFAULT_MEMORY_SAVE_URL",  # 记忆存储服务地址
    "DEFAULT_MEMORY_QUERY_URL",  # 记忆查询服务地址
    "DEFAULT_VOICEPRINT_URL",# 声纹识别服务默认地址
    "increment",             # 交互计数加一
    "reset",                 # 重置全局状态
    "get_growth_stage",      # 获取成长阶段
    "add_audio_duration",    # 增加音频时长
    "days_since_start",      # 运行天数
    "AUDIO_DATA_SECONDS",    # 累计音频秒数
    "global_state",          # 全局状态模块
    "DEFAULT_GROWTH_STAGE",  # 默认成长阶段
    "DEFAULT_PERSONALITY_VECTOR",  # 默认人格向量
    "EMOTION_STATES",        # 通用情绪列表
    "EMOTION_PROMPT_TEMPLATE",  # 情绪识别提示模板
    "MULTI_MODAL_EMOTION_PROMPT",  # 多模态情绪识别提示模板
]
