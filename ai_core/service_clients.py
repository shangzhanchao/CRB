"""Backward compatibility wrappers for service API functions.

向后兼容的服务客户端包装器，实际实现位于 :mod:`service_api`。
"""

from .service_api import (
    call_asr,
    call_tts,
    call_llm,
    call_voiceprint,
    call_memory_save,
    call_memory_query,
)

__all__ = [
    "call_asr",
    "call_tts",
    "call_llm",
    "call_voiceprint",
    "call_memory_save",
    "call_memory_query",
