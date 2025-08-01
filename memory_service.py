"""Simple memory storage service used by the Companion Robot Intelligent Brain.

提供 /save 和 /query 接口的简单服务，供 MEMORY_SAVE_URL 和
MEMORY_QUERY_URL 调用。默认把数据存入本地文件，也可切换
到 SQLite 数据库。"""

from __future__ import annotations

import json
import os
import datetime
from typing import Any, Dict, List

try:
    from fastapi import FastAPI, HTTPException  # type: ignore
    import uvicorn  # type: ignore
except Exception:  # pragma: no cover - missing deps
    FastAPI = None  # type: ignore
    HTTPException = Exception  # type: ignore
    uvicorn = None  # type: ignore

from ai_core.constants import (
    LOCAL_MEMORY_PATH,
    MEMORY_DB_PATH,
    MEMORY_SERVICE_BACKEND,
    LOG_LEVEL,
)

import logging
import sqlite3

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)

USE_DB = MEMORY_SERVICE_BACKEND == "db"

app = FastAPI() if FastAPI is not None else None


def _ensure_db(path: str = MEMORY_DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS memory (time TEXT, user_text TEXT, ai_response TEXT, mood_tag TEXT, touch_zone INTEGER, user_id TEXT)"
    )
    return conn


def save_record(record: Dict[str, Any]) -> bool:
    """Persist a memory record.

    将记忆记录保存到文件或数据库。
    """
    if USE_DB:
        conn = _ensure_db()
        conn.execute(
            "INSERT INTO memory VALUES (?, ?, ?, ?, ?, ?)",
            (
                record.get("time"),
                record.get("user_text"),
                record.get("ai_response"),
                record.get("mood_tag"),
                record.get("touch_zone"),
                record.get("user_id"),
            ),
        )
        conn.commit()
        conn.close()
    else:
        if os.path.exists(LOCAL_MEMORY_PATH):
            with open(LOCAL_MEMORY_PATH, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        else:
            data = []
        data.append(record)
        with open(LOCAL_MEMORY_PATH, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False)
    return True


def query_records(text: str, top_k: int = 3) -> List[Dict[str, Any]]:
    """Return the most relevant records containing ``text``."""
    if USE_DB:
        conn = _ensure_db()
        cur = conn.execute(
            "SELECT time, user_text, ai_response, mood_tag, touch_zone, user_id FROM memory WHERE user_text LIKE ? ORDER BY time DESC LIMIT ?",
            (f"%{text}%", top_k),
        )
        rows = [
            {
                "time": r[0],
                "user_text": r[1],
                "ai_response": r[2],
                "mood_tag": r[3],
                "touch_zone": r[4],
                "user_id": r[5],
            }
            for r in cur.fetchall()
        ]
        conn.close()
        return rows
    else:
        if not os.path.exists(LOCAL_MEMORY_PATH):
            return []
        with open(LOCAL_MEMORY_PATH, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        hits = [r for r in data if text in r.get("user_text", "")]
        return hits[:top_k]


# HTTP handlers ---------------------------------------------------------------

if app is not None:

    @app.post("/save")
    async def save_endpoint(record: Dict[str, Any]):
        """Save a memory record via HTTP."""
        try:
            record.setdefault("time", datetime.datetime.utcnow().isoformat())
            save_record(record)
            return {"ok": True}
        except Exception as exc:  # pragma: no cover - runtime error
            raise HTTPException(status_code=400, detail=str(exc))

    @app.post("/query")
    async def query_endpoint(payload: Dict[str, Any]):
        """Query saved memories by text."""
        try:
            text = str(payload.get("text", ""))
            top_k = int(payload.get("top_k", 3))
            records = query_records(text, top_k)
            return {"records": records}
        except Exception as exc:  # pragma: no cover - runtime error
            raise HTTPException(status_code=400, detail=str(exc))


def run_server(host: str = "0.0.0.0", port: int = 8001):
    """Run the memory service with Uvicorn."""
    if app is None or uvicorn is None:
        raise ImportError("FastAPI and uvicorn are required to run the service")
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":  # pragma: no cover
    run_server()