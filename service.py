"""Minimal HTTP service exposing message sending with session history.

- GET /health
- POST /interact
- POST /start_session
- GET  /session_history/{session_id}
- GET  /, /verify (minimal HTML)
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from datetime import datetime
from pathlib import Path
import sqlite3

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from ai_core.intelligent_core import IntelligentCore
from services.session_service import SessionService
from ai_core.constants import DEFAULT_SESSION_LIMIT


core = IntelligentCore()
session_service = SessionService(core)

# persistent storage for session history: reuse existing memory database
BASE_DIR = Path(__file__).resolve().parent
# store session history table inside the enhanced memory system DB
HISTORY_DB_PATH = BASE_DIR / "enhanced_memory.db"

app = FastAPI(title="CRB Minimal API", version="1.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def handle_request(data: Dict[str, Any]) -> Dict[str, Any]:
    return session_service.handle_request(data)


class SessionHistoryStore:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self._ensure_tables()

    def _ensure_tables(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS session_history (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  session_id TEXT NOT NULL,
                  ts TEXT NOT NULL,
                  type TEXT NOT NULL,
                  input_text TEXT,
                  reply_text TEXT
                )
                """
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_session_ts ON session_history(session_id, ts)"
            )
            # 确保数据库连接设置正确
            conn.execute("PRAGMA foreign_keys = ON")

    def add(self, session_id: str, record: Dict[str, Any]) -> None:
        if not session_id:
            return
        ts = datetime.now().isoformat()
        rec_type = str(record.get("type", "interact"))
        input_text = record.get("input_text")
        reply_text = record.get("reply_text")
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO session_history(session_id, ts, type, input_text, reply_text) VALUES(?,?,?,?,?)",
                (session_id, ts, rec_type, input_text, reply_text),
            )

    def get(self, session_id: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        if not session_id:
            return []
        query = "SELECT ts, type, input_text, reply_text FROM session_history WHERE session_id=? ORDER BY ts DESC"
        params: tuple = (session_id,)
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(query, params).fetchall()
        items = [
            {"timestamp": r[0], "type": r[1], "input_text": r[2] or "", "reply_text": r[3] or ""}
            for r in rows
        ]
        if limit and limit > 0:
            return items[:limit]
        return items

    def total(self, session_id: str) -> int:
        if not session_id:
            return 0
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT COUNT(*) FROM session_history WHERE session_id=?", (session_id,)
            ).fetchone()
        return int(row[0]) if row else 0


history = SessionHistoryStore(HISTORY_DB_PATH)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "crb-minimal",
        "timestamp": datetime.now().isoformat(),
    }


@app.post("/interact")
async def interact(payload: Dict[str, Any]):
    try:
        # 使用机器人ID作为会话ID（一个机器人对应一个会话）
        robot_id = (payload.get("robot_id") or "robotA").strip()
        sess = (payload.get("session_id") or robot_id).strip()
        payload["session_id"] = sess

        result = session_service.handle_request(payload)
        # 以机器人ID固定会话ID
        result["session_id"] = sess
        if sess:
            history.add(sess, {
                "type": "interact",
                "input_text": payload.get("text") or "",
                "reply_text": result.get("text") or "",
            })
        return JSONResponse(result)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/start_session")
async def start_session(payload: Dict[str, Any] | None = None):
    try:
        robot_id = "robotA"
        if payload and isinstance(payload, dict):
            robot_id = (payload.get("robot_id") or robot_id).strip()
        # 一个机器人一个会话：将会话ID固定为 robot_id
        core.start_session(session_id=robot_id)
        return {"success": True, "session_id": robot_id}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/session_history/{session_id}")
async def get_session_history(session_id: str, limit: int = DEFAULT_SESSION_LIMIT):
    try:
        records = history.get(session_id, limit=limit)
        return {
            "success": True,
            "session_id": session_id,
            "total": history.total(session_id),
            "returned": len(records),
            "records": records,
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/")
async def root():
    return HTMLResponse("""
    <!doctype html>
    <html lang="zh-CN">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
             <title>CRB 陪伴机器人大脑验证系统</title>
    </head>
    <body>
      <h2>CRB 陪伴机器人大脑验证系统</h2>
      <p>验证陪伴机器人的智能大脑功能，支持情感交互、记忆学习和个性化对话。</p>
      <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 900px; margin: 32px auto; padding: 0 20px; background: #f8fafc; }
        .card { background: #fff; border: 1px solid #e5e7eb; border-radius: 12px; box-shadow: 0 6px 20px rgba(2,6,23,.06); padding: 18px; }
                 .group { margin-bottom: 14px; }
         label { display: block; color: #374151; margin-bottom: 8px; font-weight: 600; font-size: 15px; }
         input[type="text"] { width: 100%; padding: 12px 16px; border: 2px solid #e5e7eb; border-radius: 10px; font-size: 15px; transition: border-color 0.2s; box-sizing: border-box; }
         input[type="text"]:focus { outline: none; border-color: #2563eb; box-shadow: 0 0 0 3px rgba(37,99,235,0.1); }
         .input-container { display: flex; gap: 12px; align-items: flex-start; }
         .input-main { flex: 1; }
         .input-buttons { display: flex; flex-direction: column; gap: 8px; }
         .media-btn { width: 48px; height: 48px; border: 2px solid #e5e7eb; border-radius: 10px; background: #fff; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 20px; transition: all 0.2s; }
         .media-btn:hover { border-color: #2563eb; background: #f8fafc; }
         .media-btn.active { border-color: #2563eb; background: #dbeafe; color: #2563eb; }
         textarea { width: 100%; padding: 16px 20px; border: 2px solid #e5e7eb; border-radius: 12px; font-size: 16px; line-height: 1.5; min-height: 80px; resize: vertical; transition: border-color 0.2s; box-sizing: border-box; font-family: inherit; }
         textarea:focus { outline: none; border-color: #2563eb; box-shadow: 0 0 0 3px rgba(37,99,235,0.1); }
        small.hint { display: block; color: #6b7280; margin-top: 4px; }
        ul#zones { list-style: none; padding: 0; margin: 8px 0; display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; }
        ul#zones li { background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 8px; padding: 8px 10px; }
        .center { text-align: center; }
        button#send { padding: 12px 24px; font-weight: 600; border: 0; border-radius: 12px; background: #2563eb; color: #fff; cursor: pointer; font-size: 16px; transition: background 0.2s; }
        button#send:hover { background: #1d4ed8; }
        pre#out { white-space: pre-wrap; background: #0f172a; color: #e2e8f0; padding: 16px; border-radius: 10px; overflow: auto; font-family: 'SF Mono', Monaco, 'Cascadia Code', monospace; }
        h2 { color: #1e293b; margin-bottom: 8px; }
        p { color: #64748b; margin-bottom: 24px; }
                 .history-container { background: #fff; border: 1px solid #e5e7eb; border-radius: 12px; padding: 16px; }
         .history-list { list-style: none; padding: 0; margin: 0; max-height: 400px; overflow-y: auto; }
         .history-list::-webkit-scrollbar { width: 8px; }
         .history-list::-webkit-scrollbar-track { background: #f1f5f9; border-radius: 4px; }
         .history-list::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
         .history-list::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
         .history-item { padding: 12px; margin-bottom: 12px; background: #f8fafc; border-radius: 8px; border-left: 4px solid #2563eb; }
         .history-item:last-child { margin-bottom: 0; }
         .history-timestamp { color: #6b7280; font-size: 12px; margin-bottom: 4px; }
         .history-user { color: #1e293b; font-weight: 600; margin-bottom: 4px; }
         .history-ai { color: #059669; font-weight: 600; margin-bottom: 4px; }
         .history-text { color: #374151; line-height: 1.5; }
        .response-container { background: #fff; border: 1px solid #e5e7eb; border-radius: 12px; padding: 16px; }
        .response-header { display: flex; align-items: center; margin-bottom: 12px; }
        .response-icon { width: 24px; height: 24px; background: #2563eb; border-radius: 50%; margin-right: 8px; display: flex; align-items: center; justify-content: center; color: white; font-size: 12px; }
        .response-title { color: #1e293b; font-weight: 600; margin: 0; }
        .response-content { background: #f8fafc; border-radius: 8px; padding: 12px; font-family: 'SF Mono', Monaco, 'Cascadia Code', monospace; font-size: 14px; line-height: 1.5; }
        .response-json { color: #059669; }
        .response-text { color: #1e293b; font-weight: 500; }
        .response-emotion { color: #7c3aed; }
        .response-action { color: #dc2626; }
                 .response-expression { color: #ea580c; }
         .summary-container { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; padding: 20px; margin: 24px 0; color: white; }
         .summary-header { display: flex; align-items: center; margin-bottom: 16px; }
         .summary-icon { width: 32px; height: 32px; background: rgba(255,255,255,0.2); border-radius: 50%; margin-right: 12px; display: flex; align-items: center; justify-content: center; font-size: 16px; }
         .summary-title { color: white; font-weight: 600; margin: 0; font-size: 18px; }
         .summary-content { line-height: 1.6; font-size: 15px; opacity: 0.95; }
         .summary-highlight { background: rgba(255,255,255,0.15); padding: 2px 6px; border-radius: 4px; font-weight: 500; }
       </style>
       <div class="card">
        <div class="group">
          <label for="robot">机器人标识</label>
          <input id="robot" value="robotA" />
          <small class="hint">用于区分不同的机器人实例，每个机器人拥有独立的对话历史</small>
        </div>
        <div class="group">
          <label for="text">对话内容</label>
          <div class="input-container">
            <div class="input-main">
              <textarea id="text" placeholder="输入你想说的话，机器人会出不同的回应..."></textarea>
            </div>
            <div class="input-buttons">
              <button class="media-btn" id="voiceBtn" title="语音输入">
                <span>🎤</span>
              </button>
              <button class="media-btn" id="videoBtn" title="视频通话">
                <span>📹</span>
              </button>
            </div>
          </div>
          <small class="hint">支持文字、语音、视频多种交互方式，按 Ctrl+Enter 快速发送</small>
        </div>
        <div class="group">
          <label>触摸区域</label>
          <ul id="zones">
            <li><label><input type="radio" name="touchZone" value="0" checked> 头部</label></li>
            <li><label><input type="radio" name="touchZone" value="1"> 背后</label></li>
            <li><label><input type="radio" name="touchZone" value="2"> 胸口</label></li>
          </ul>
          <small class="hint">不同触摸区域会触发不同的情感反应和回复模式</small>
        </div>

        <div class="center" style="margin-top:10px;">
          <button id="send">发送消息</button>
        </div>
      </div>
        <div style="margin-top:24px">
        <div class="response-container">
          <div class="response-header">
            <div class="response-icon">🤖</div>
            <h3 class="response-title">机器人回复</h3>
          </div>
          <div class="response-content">
            <pre id="out">等待发送...</pre>
          </div>
                 </div>
       </div>
       <div class="summary-container">
         <div class="summary-header">
           <div class="summary-icon">🧠</div>
           <h3 class="summary-title">智能大脑处理流程</h3>
         </div>
         <div class="summary-content">
           陪伴机器人通过 <span class="summary-highlight">文字输入</span>、<span class="summary-highlight">语音识别</span>、<span class="summary-highlight">视频感知</span> 和 <span class="summary-highlight">触摸交互</span> 等多种方式接收用户信息，经过智能大脑的深度学习算法处理后，机器人会输出 <span class="summary-highlight">文本回复</span>（可转换为语音）、<span class="summary-highlight">动作指令</span>（控制肢体表达情感）和 <span class="summary-highlight">表情指令</span>（面部屏幕或眼睛的情绪动画），实现自然、温暖的人机交互体验。
         </div>
       </div>
       <div style="margin-top:24px">
         <div class="history-container">
          <h3>对话历史</h3>
          <div id="history">暂无记录</div>
        </div>
      </div>
      <script>
      (function(){
        const $ = (id) => document.getElementById(id);
        async function refreshHistory(){
          const sid = currentSessionId;
          if(!sid){ $('history').textContent = '请先设置机器人标识'; return; }
          $('history').textContent = '加载中...';
          try{
                         const res = await fetch('/session_history/' + encodeURIComponent(sid) + '?limit=50');
            const data = await res.json();
            if(!data.success){ $('history').textContent = '获取失败'; return; }
            const list = data.records || [];
            if(list.length === 0){ $('history').textContent = '暂无记录'; return; }
                         const html = '<ul class="history-list">' + list.map(r => {
               const t = r.timestamp ? r.timestamp.replace('T', ' ').substring(0, 19) : '';
               const input = (r.input_text||'').replace(/</g,'&lt;');
               const reply = (r.reply_text||'').replace(/</g,'&lt;');
               return `<li class="history-item">
                 <div class="history-timestamp">${t}</div>
                 <div class="history-user">你: ${input}</div>
                 <div class="history-ai">AI: ${reply}</div>
               </li>`;
             }).join('') + '</ul>';
            $('history').innerHTML = html;
          }catch(e){
            $('history').textContent = '获取失败: ' + (e && e.message ? e.message : String(e));
          }
        }
        // 会话ID现在直接使用机器人ID，无需同步
        let currentSessionId = $('robot').value.trim() || 'robotA';
        
        $('robot').addEventListener('input', function() {
          currentSessionId = $('robot').value.trim() || 'robotA';
        });

        // 支持 Ctrl+Enter 发送消息
        $('text').addEventListener('keydown', function(e) {
          if (e.ctrlKey && e.key === 'Enter') {
            e.preventDefault();
            $('send').click();
          }
        });

        // 语音按钮事件处理
        $('voiceBtn').addEventListener('click', function() {
          this.classList.toggle('active');
          if (this.classList.contains('active')) {
            this.innerHTML = '<span>⏹️</span>';
            this.title = '停止录音';
            // 这里可以添加语音录制逻辑
            console.log('开始语音录制...');
          } else {
            this.innerHTML = '<span>🎤</span>';
            this.title = '语音输入';
            // 这里可以添加停止录制逻辑
            console.log('停止语音录制...');
          }
        });

        // 视频按钮事件处理
        $('videoBtn').addEventListener('click', function() {
          this.classList.toggle('active');
          if (this.classList.contains('active')) {
            this.innerHTML = '<span>📷</span>';
            this.title = '结束视频';
            // 这里可以添加视频通话逻辑
            console.log('开始视频通话...');
          } else {
            this.innerHTML = '<span>📹</span>';
            this.title = '视频通话';
            // 这里可以添加结束通话逻辑
            console.log('结束视频通话...');
          }
        });

        // 页面不再提供按钮，仍在初始化时自动获取会话并刷新
        $('send').addEventListener('click', async function(){
          const payload = {
            robot_id: $('robot').value || 'robotA',
            text: $('text').value || ''
          };
          const radios = document.querySelectorAll('input[name="touchZone"]');
          let selectedZone = null;
          radios.forEach(r => { if (r.checked) selectedZone = parseInt(r.value, 10); });
          if (selectedZone !== null && !Number.isNaN(selectedZone)) {
            payload.touch_zone = selectedZone;
          }
          payload.session_id = currentSessionId;
          $('out').textContent = '发送中...';
          try{
            const res = await fetch('/interact', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(payload)
            });
            const data = await res.json();
            // 格式化显示机器人回复
            let displayText = '';
            if (data.text) {
              try {
                const jsonData = JSON.parse(data.text);
                displayText = `{
  <span class="response-json">"text"</span>: <span class="response-text">"${jsonData.text || ''}"</span>,
  <span class="response-json">"emotion"</span>: <span class="response-emotion">"${jsonData.emotion || ''}"</span>,
  <span class="response-json">"action"</span>: <span class="response-action">${JSON.stringify(jsonData.action || [])}</span>,
  <span class="response-json">"expression"</span>: <span class="response-expression">"${jsonData.expression || ''}"</span>
}`;
              } catch (e) {
                displayText = data.text;
              }
            } else {
              displayText = JSON.stringify(data, null, 2);
            }
            $('out').innerHTML = displayText;
            // 会话ID现在直接使用机器人ID，无需更新
            await refreshHistory();
          }catch(e){
            $('out').textContent = '请求失败: ' + (e && e.message ? e.message : String(e));
          }
        });

        // 页面加载后：自动刷新会话记录
        (async function initHistory(){
          try{
            await refreshHistory();
          }catch(e){
            // ignore errors on init
          }
        })();
      })();
      </script>
    </body>
    </html>
    """)


@app.get("/verify")
async def verify():
    return await root()


def run_server(host: str = "127.0.0.1", port: int = 8000):
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    run_server()


