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
import asyncio
from typing import Any, Dict, Optional

from .constants import (
    DEFAULT_ASR_URL,
    DEFAULT_TTS_URL,
    DEFAULT_LLM_URL,
    DEFAULT_VOICEPRINT_URL,
    DEFAULT_MEMORY_SAVE_URL,
    DEFAULT_MEMORY_QUERY_URL,
    LOCAL_MEMORY_PATH,
    LOG_LEVEL,
)
from ai_core.constants import HISTORY_MAX_RECORDS
from .qwen_service import get_qwen_service
from .doubao_service import get_doubao_service

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


async def _post_async(url: str, payload: Dict[str, Any], timeout: int = 5) -> Optional[Dict[str, Any]]:
    """Async wrapper for :func:`_post` using a thread."""

    return await asyncio.to_thread(_post, url, payload, timeout)


def call_asr(audio_path: str, url: str = DEFAULT_ASR_URL) -> str:
    """Call ASR service and return transcribed text.

    调用语音识别服务，若失败则返回文件名（不含扩展名）。
    """
    if url is None:
        # 使用本地ASR或返回文件名
        return os.path.splitext(os.path.basename(audio_path))[0]
    
    res = _post(url, {"path": audio_path})
    if res and isinstance(res.get("text"), str):
        return res["text"]
    return os.path.splitext(os.path.basename(audio_path))[0]


async def async_call_asr(audio_path: str, url: str = DEFAULT_ASR_URL) -> str:
    """Asynchronous version of :func:`call_asr`.

    :func:`call_asr` 的异步版本，便于高度并发场景下使用。
    """

    return await asyncio.to_thread(call_asr, audio_path, url)


def call_tts(text: str, url: str = DEFAULT_TTS_URL) -> str:
    """Call TTS service and get audio URL.

    调用语音合成服务，失败则返回空字符串。
    """
    if url is None:
        # 使用本地TTS或返回空字符串
        return ""
    
    res = _post(url, {"text": text})
    if res and isinstance(res.get("audio_url"), str):
        return res["audio_url"]
    return ""


async def async_call_tts(text: str, url: str = DEFAULT_TTS_URL) -> str:
    """Asynchronous version of :func:`call_tts`.

    用于语音同步生成之异步调用，可防止 I/O 阻塞。
    """

    return await asyncio.to_thread(call_tts, text, url)


def call_llm(prompt: str, url: str = None) -> str:
    """调用LLM服务
    
    Parameters
    ----------
    prompt : str
        发送给模型的提示词
    url : str
        模型服务类型，支持 'doubao' 等
        
    Returns
    -------
    str
        模型返回的文本内容
    """
    if url == "doubao":
        service = get_doubao_service()
        return service._call_sync(prompt, system_prompt=None, history=None)
    else:
        logger.warning(f"call_llm: 未实现的模型类型 {url}")
        return ""


async def async_call_llm(prompt: str, url: str = None) -> str:
    """异步调用LLM服务
    
    Parameters
    ----------
    prompt : str
        发送给模型的提示词
    url : str
        模型服务类型，支持 'doubao' 等
        
    Returns
    -------
    str
        模型返回的文本内容
    """
    if url == "doubao":
        service = get_doubao_service()
        return await service.call(prompt, system_prompt=None, history=None)
    else:
        logger.warning(f"async_call_llm: 未实现的模型类型 {url}")
        return ""


def call_llm_stream(prompt: str, url: str = None):
    """流式调用LLM服务
    
    Parameters
    ----------
    prompt : str
        发送给模型的提示词
    url : str
        模型服务类型，支持 'doubao' 等
        
    Returns
    -------
    AsyncGenerator
        流式返回的文本内容
    """
    if url == "doubao":
        service = get_doubao_service()
        return service.stream(prompt, system_prompt=None, history=None)
    else:
        logger.warning(f"call_llm_stream: 未实现的模型类型 {url}")
        return None


def call_voiceprint(audio_path: str, url: str = DEFAULT_VOICEPRINT_URL) -> str:
    """Recognize speaker from voiceprint service.

    调用声纹识别服务识别说话人，失败时返回文件名或 ``unknown``。
    """
    if url is None:
        # 使用本地声纹识别或返回文件名
        name = os.path.splitext(os.path.basename(audio_path))[0]
        return name or "unknown"
    
    res = _post(url, {"path": audio_path})
    if res and isinstance(res.get("user_id"), str):
        return res["user_id"]
    name = os.path.splitext(os.path.basename(audio_path))[0]
    return name or "unknown"


async def async_call_voiceprint(audio_path: str, url: str = DEFAULT_VOICEPRINT_URL) -> str:
    """Asynchronous version of :func:`call_voiceprint`.

    对声纹识别依赖网络请求时非常有用。
    """

    return await asyncio.to_thread(call_voiceprint, audio_path, url)


def call_memory_save(
    record: Dict[str, Any],
    url: str = DEFAULT_MEMORY_SAVE_URL,
    fallback_path: str = LOCAL_MEMORY_PATH,
) -> bool:
    """Save a memory record via HTTP with local fallback.

    通过 HTTP 将记忆记录发送到远程服务，若失败则写入本地备份文件。
    """
    prepared = {
        k: (v.isoformat() if isinstance(v, datetime.datetime) else v)
        for k, v in record.items()
    }
    res = _post(url, prepared) if url else None
    if res and res.get("ok"):
        return True
    else:
        logger.warning(
            "Memory service unavailable, storing record locally at %s", fallback_path
        )
    try:
        if os.path.exists(fallback_path):
            with open(fallback_path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        else:
            data = []
        data.append(prepared)
        with open(fallback_path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False)
        logger.debug("Memory saved locally to %s", fallback_path)
    except Exception as exc:  # pragma: no cover - 文件写入失败
        logger.warning("Local memory save failed: %s", exc)
    return False


async def async_call_memory_save(
    record: Dict[str, Any],
    url: str = DEFAULT_MEMORY_SAVE_URL,
    fallback_path: str = LOCAL_MEMORY_PATH,
) -> bool:
    """Asynchronous wrapper for :func:`call_memory_save`.

    将记录以异步方式传输至记忆服务，避免网络阻塞导致程序停止等待。
    """

    return await asyncio.to_thread(call_memory_save, record, url, fallback_path)


def call_memory_query(
    prompt: str,
    top_k: int = HISTORY_MAX_RECORDS,
    url: str = DEFAULT_MEMORY_QUERY_URL,
    fallback_path: str = LOCAL_MEMORY_PATH,
) -> Optional[list[Dict[str, Any]]]:
    """Query memory service with a local file fallback.

    调用远程记忆查询服务，失败时从本地备份文件中检索相关记录。
    """
    res = _post(url, {"text": prompt, "top_k": top_k}) if url else None
    if res and isinstance(res.get("records"), list):
        return res["records"]
    try:
        with open(fallback_path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        return None
    hits = [r for r in data if prompt in r.get("user_text", "")]
    return hits[:top_k]


async def async_call_memory_query(
    prompt: str,
    top_k: int = HISTORY_MAX_RECORDS,
    url: str = DEFAULT_MEMORY_QUERY_URL,
    fallback_path: str = LOCAL_MEMORY_PATH,
) -> Optional[list[Dict[str, Any]]]:
    """Asynchronous wrapper for :func:`call_memory_query`.

    在多并发场景下可以实现更多请求的异步处理。
    """

    return await asyncio.to_thread(
        call_memory_query, prompt, top_k, url, fallback_path
    )