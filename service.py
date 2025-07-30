"""Asynchronous HTTP service for the companion robot brain.

基于 FastAPI 的异步 HTTP 服务入口，可统一处理外部请求。

Example request JSON::
    {"robot_id": "robotA", "text": "hello"}
"""

from __future__ import annotations

import json
from typing import Any, Dict

try:
    from fastapi import FastAPI, HTTPException  # type: ignore
    import uvicorn  # type: ignore
except Exception:  # pragma: no cover - library missing
    FastAPI = None  # type: ignore
    HTTPException = Exception  # type: ignore
    uvicorn = None  # type: ignore

from ai_core import IntelligentCore, UserInput

core = IntelligentCore()


def handle_request(payload: Dict[str, Any]):
    """Process a JSON payload and return AI response dict.

    处理 JSON 请求并返回包含文本、音频、动作和表情的结果。
    """
    robot_id = payload.get("robot_id", "")
    text = payload.get("text")
    audio = payload.get("audio_path")
    image = payload.get("image_path")
    video = payload.get("video_path")
    zone = payload.get("touch_zone")
    user = UserInput(
        audio_path=audio,
        image_path=image,
        video_path=video,
        text=text,
        robot_id=robot_id,
        touch_zone=zone,
    )
    reply = core.process(user)
    return reply.as_dict()


app = FastAPI() if FastAPI is not None else None


if app is not None:
    @app.post("/interact")
    async def interact(payload: Dict[str, Any]):
        """Async HTTP endpoint bridging to :func:`handle_request`.

        异步网络接口，将请求转发给 :func:`handle_request`。
        """
        try:
            return handle_request(payload)
        except Exception as exc:  # pragma: no cover - runtime error
            raise HTTPException(status_code=400, detail=str(exc))


def run_server(host: str = "0.0.0.0", port: int = 8000):
    """Start the FastAPI server using Uvicorn.

    启动 FastAPI 服务，连接外网使用 Uvicorn 执行。
    """
    if app is None or uvicorn is None:
        raise ImportError("FastAPI and uvicorn are required to run the service")
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":  # pragma: no cover
    run_server()
