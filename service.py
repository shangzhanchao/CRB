"""Simple HTTP entry point for the companion robot brain.

简易 HTTP 服务入口，统一处理外部请求。

Example request JSON::
    {"robot_id": "robotA", "text": "hello"}
"""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Dict

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


class _Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/interact":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", 0))
        data = self.rfile.read(length).decode("utf-8")
        payload = json.loads(data or "{}")
        try:
            result = handle_request(payload)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode("utf-8"))
        except Exception as exc:  # pragma: no cover - runtime error
            self.send_response(400)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(exc)}).encode("utf-8"))


def run_server(host: str = "0.0.0.0", port: int = 8000):
    """Start the HTTP server."""
    with HTTPServer((host, port), _Handler) as httpd:
        print(f"Serving on {host}:{port} ...")
        httpd.serve_forever()


if __name__ == "__main__":  # pragma: no cover
    run_server()
