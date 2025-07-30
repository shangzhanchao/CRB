"""External service API wrappers.

封装外部服务的调用方法，包括 ASR、TTS、LLM、声纹识别以及记忆存储和查询。
这些函数在网络请求失败时会提供简易回退，以便离线测试。
"""

from __future__ import annotations

import json
import datetime
import os
import urllib.request
import logging
from typing import Any, Dict, Optional

from .constants import (
    DEFAULT_ASR_URL,
    DEFAULT_TTS_URL,
    DEFAULT_LLM_URL,
    DEFAULT_VOICEPRINT_URL,
    DEFAULT_MEMORY_SAVE_URL,
    DEFAULT_MEMORY_QUERY_URL,
    LOG_LEVEL,
)

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)


def _post(url: str, payload: Dict[str, Any], timeout: int = 5) -> Optional[Dict[str, Any]]:
    """Send JSON payload to ``url`` and return the JSON result.

    发送 JSON 数据到指定 ``url``，返回解析后的结果；若请求失败则返回 ``None``。
    """
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            text = resp.read().decode("utf-8")
            logger.debug("%s response: %s", url, text)
            return json.loads(text)
    except Exception as exc:  # pragma: no cover - 网络错误
        logger.warning("Request to %s failed: %s", url, exc)
        return None


def call_asr(audio_path: str, url: str = DEFAULT_ASR_URL) -> str:
    """Call ASR service and return transcribed text.

    调用语音识别服务，若失败则返回文件名（不含扩展名）。
    """
    res = _post(url, {"path": audio_path})
    if res and isinstance(res.get("text"), str):
        return res["text"]
    return os.path.splitext(os.path.basename(audio_path))[0]


def call_tts(text: str, url: str = DEFAULT_TTS_URL) -> str:
    """Call TTS service and get audio URL.

    调用语音合成服务，失败则返回空字符串。
    """
    res = _post(url, {"text": text})
    if res and isinstance(res.get("audio_url"), str):
        return res["audio_url"]
    return ""


def call_llm(prompt: str, url: str = DEFAULT_LLM_URL) -> str:
    """Request completion from LLM service.

    调用大模型服务生成文本，失败则返回空字符串。
    """
    res = _post(url, {"prompt": prompt})
    if res and isinstance(res.get("text"), str):
        return res["text"]
    return ""


def call_voiceprint(audio_path: str, url: str = DEFAULT_VOICEPRINT_URL) -> str:
    """Recognize speaker from voiceprint service.

    调用声纹识别服务识别说话人，失败时返回文件名或 ``unknown``。
    """
    res = _post(url, {"path": audio_path})
    if res and isinstance(res.get("user_id"), str):
        return res["user_id"]
    name = os.path.splitext(os.path.basename(audio_path))[0]
    return name or "unknown"


def call_memory_save(record: Dict[str, Any], url: str = DEFAULT_MEMORY_SAVE_URL) -> bool:
    """Save a memory record via HTTP.

    通过 HTTP 将记忆记录发送到远程服务。失败则返回 ``False``。
    """
    prepared = {k: (v.isoformat() if isinstance(v, datetime.datetime) else v) for k, v in record.items()}
    res = _post(url, prepared)
    return bool(res and res.get("ok"))


def call_memory_query(prompt: str, top_k: int = 3, url: str = DEFAULT_MEMORY_QUERY_URL) -> Optional[list[Dict[str, Any]]]:
    """Query memory service for related records.

    调用记忆查询服务以获取与 ``prompt`` 最相关的历史记录列表。
    """
    res = _post(url, {"text": prompt, "top_k": top_k})
    if res and isinstance(res.get("records"), list):
        return res["records"]
    return None
