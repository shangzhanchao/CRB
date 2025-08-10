"""Session service for handling session management and interactions."""

from typing import Dict, Any, Optional
from ai_core.intelligent_core import IntelligentCore, UserInput


class SessionService:
    """Service for handling session management and interactions."""
    
    def __init__(self, core: IntelligentCore):
        self.core = core
    
    def handle_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Process a JSON payload and return AI response dict."""
        try:
            robot_id = payload.get("robot_id", "")
            text = payload.get("text")
            audio = payload.get("audio_path")
            image = payload.get("image_path")
            video = payload.get("video_path")
            zone = payload.get("touch_zone")
            session_id = payload.get("session_id")
            
            user = UserInput(
                audio_path=audio,
                image_path=image,
                video_path=video,
                text=text,
                robot_id=robot_id,
                touch_zone=zone,
                session_id=session_id,
            )
            
            reply = self.core.process(user)
            return reply.as_dict()
        except Exception as e:
            print(f"处理请求时出错: {e}")
            raise
    
    async def handle_websocket_interaction(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle WebSocket interaction message."""
        try:
            # 提取消息数据
            robot_id = message.get("robot_id", "")
            text = message.get("text", "")
            audio_path = message.get("audio_path")
            image_path = message.get("image_path")
            video_path = message.get("video_path")
            touch_zone = message.get("touch_zone")
            session_id = message.get("session_id")
            
            # 创建用户输入
            user = UserInput(
                audio_path=audio_path,
                image_path=image_path,
                video_path=video_path,
                text=text,
                robot_id=robot_id,
                touch_zone=touch_zone,
                session_id=session_id,
            )
            
            # 处理请求
            reply = self.core.process(user)
            return reply.as_dict()
            
        except Exception as e:
            print(f"WebSocket交互处理失败: {e}")
            return {"error": str(e)}
    
    async def start_session(self) -> str:
        """Start a new session."""
        try:
            session_id = self.core.start_session()
            return session_id
        except Exception as e:
            raise Exception(f"开始会话失败: {e}")
    
    async def clear_session(self) -> int:
        """Clear session memory."""
        try:
            # 清除当前会话的记忆
            removed_count = self.core.clear_session_memory()
            return removed_count
        except Exception as e:
            raise Exception(f"清除会话失败: {e}")
    
    async def get_session_info(self, session_id: str) -> Dict[str, Any]:
        """Get session information."""
        try:
            # 这里应该实现获取会话信息的逻辑
            # 暂时返回基本信息
            return {
                "session_id": session_id,
                "status": "active",
                "created_time": "2024-01-01T00:00:00Z",
                "interaction_count": 0,
                "memory_count": 0
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def parse_touch_zone(self, touch_zone: str) -> Optional[int]:
        """Parse touch zone string to integer.
        
        抚摸区域参数定义：
        0 = 头部 (head)
        1 = 背后 (back) 
        2 = 胸口 (chest)
        """
        if not touch_zone or not touch_zone.strip():
            return 0  # 默认头部
        
        try:
            zone = int(touch_zone)
            # 验证抚摸区域参数
            if zone not in [0, 1, 2]:
                print(f"警告: 无效的抚摸区域参数 {zone}，使用默认值 0 (头部)")
                return 0
            return zone
        except ValueError:
            print(f"警告: 无法解析抚摸区域参数 '{touch_zone}'，使用默认值 0 (头部)")
            return 0
    
    def validate_session_id(self, session_id: str) -> bool:
        """Validate session ID format."""
        if not session_id:
            return False
        
        # 简单的会话ID验证
        return session_id.startswith("session_") and len(session_id) > 10
    
    def get_session_stats(self, session_id: str) -> Dict[str, Any]:
        """Get session statistics."""
        try:
            # 这里应该实现获取会话统计信息的逻辑
            return {
                "session_id": session_id,
                "total_interactions": 0,
                "total_memories": 0,
                "average_response_time": 0.0,
                "emotion_distribution": {},
                "last_interaction": None
            }
        except Exception as e:
            return {"error": str(e)} 