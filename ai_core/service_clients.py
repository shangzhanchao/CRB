"""Utility functions for external AI services.

This module contains lightweight wrappers that attempt to access
remote services for ASR, TTS, LLM and voiceprint recognition. If the
HTTP request fails (e.g. service unreachable), a simple fallback is
used so tests can run offline.
"""

from __future__ import annotations

import json
import os
import urllib.request
import urllib.error
import logging
from typing import Any, Dict, Optional

from .constants import (
    DEFAULT_TTS_URL,
    DEFAULT_ASR_URL,
    DEFAULT_LLM_URL,
    DEFAULT_VOICEPRINT_URL,
    LOG_LEVEL,
)

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)


def _post(url: str, payload: Dict[str, Any], timeout: int = 5) -> Optional[Dict[str, Any]]:
    """Send a JSON POST request and return parsed JSON response.

    If the request fails, ``None`` is returned so the caller can fall back
    to a deterministic local result.
    """

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            text = resp.read().decode("utf-8")
            logger.debug("%s response: %s", url, text)
            return json.loads(text)
    except Exception as exc:  # pragma: no cover - network error
        logger.warning("Request to %s failed: %s", url, exc)
        return None


def call_asr(audio_path: str, url: str = DEFAULT_ASR_URL) -> str:
    """Send audio to ASR service and return transcribed text.

    If the service call fails, the file name without extension is used as
    the fallback transcription.
    """

    res = _post(url, {"path": audio_path})
    if res and isinstance(res.get("text"), str):
        return res["text"]
    return os.path.splitext(os.path.basename(audio_path))[0]


def call_tts(text: str, url: str = DEFAULT_TTS_URL) -> str:
    """Send text to TTS service and return an audio URL.

    When offline or failing, an empty string is returned.
    """

    res = _post(url, {"text": text})
    if res and isinstance(res.get("audio_url"), str):
        return res["audio_url"]
    return ""


def call_llm(prompt: str, url: str = DEFAULT_LLM_URL) -> str:
    """Request a completion from the LLM service.

    On failure, an empty string is returned so the caller can decide on a
    fallback message.
    """

    res = _post(url, {"prompt": prompt})
    if res and isinstance(res.get("text"), str):
        return res["text"]
    return ""


def call_voiceprint(audio_path: str, url: str = DEFAULT_VOICEPRINT_URL) -> str:
    """Recognize speaker identity from the given audio.

    If the remote service is unreachable, the base file name is returned.
    """

    res = _post(url, {"path": audio_path})
    if res and isinstance(res.get("user_id"), str):
        return res["user_id"]
    name = os.path.splitext(os.path.basename(audio_path))[0]
    return name or "unknown"
