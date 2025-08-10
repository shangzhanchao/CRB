"""
专业日志输出工具模块

提供统一的日志输出格式，去掉表情符号，使用规范和专业的方式输出日志信息。
"""

import logging
from datetime import datetime
from typing import Any, Dict, Optional


class ProfessionalLogger:
    """专业日志输出类"""
    
    def __init__(self, name: str = "CRB"):
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # 如果没有处理器，添加一个
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def info(self, message: str, details: Optional[Dict[str, Any]] = None):
        """输出信息日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[INFO] {timestamp} - {message}")
        if details:
            for key, value in details.items():
                print(f"        {key}: {value}")
    
    def success(self, message: str, details: Optional[Dict[str, Any]] = None):
        """输出成功日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[SUCCESS] {timestamp} - {message}")
        if details:
            for key, value in details.items():
                print(f"           {key}: {value}")
    
    def error(self, message: str, error: Optional[Exception] = None):
        """输出错误日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[ERROR] {timestamp} - {message}")
        if error:
            print(f"        Error: {str(error)}")
    
    def warning(self, message: str, details: Optional[Dict[str, Any]] = None):
        """输出警告日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[WARNING] {timestamp} - {message}")
        if details:
            for key, value in details.items():
                print(f"            {key}: {value}")
    
    def processing(self, message: str, details: Optional[Dict[str, Any]] = None):
        """输出处理日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[PROCESSING] {timestamp} - {message}")
        if details:
            for key, value in details.items():
                print(f"              {key}: {value}")
    
    def debug(self, message: str, details: Optional[Dict[str, Any]] = None):
        """输出调试日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[DEBUG] {timestamp} - {message}")
        if details:
            for key, value in details.items():
                print(f"       {key}: {value}")
    
    def test(self, message: str, details: Optional[Dict[str, Any]] = None):
        """输出测试日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[TEST] {timestamp} - {message}")
        if details:
            for key, value in details.items():
                print(f"      {key}: {value}")


# 创建全局日志实例
logger = ProfessionalLogger("CRB")


def log_info(message: str, details: Optional[Dict[str, Any]] = None):
    """输出信息日志"""
    logger.info(message, details)


def log_success(message: str, details: Optional[Dict[str, Any]] = None):
    """输出成功日志"""
    logger.success(message, details)


def log_error(message: str, error: Optional[Exception] = None):
    """输出错误日志"""
    logger.error(message, error)


def log_warning(message: str, details: Optional[Dict[str, Any]] = None):
    """输出警告日志"""
    logger.warning(message, details)


def log_processing(message: str, details: Optional[Dict[str, Any]] = None):
    """输出处理日志"""
    logger.processing(message, details)


def log_debug(message: str, details: Optional[Dict[str, Any]] = None):
    """输出调试日志"""
    logger.debug(message, details)


def log_test(message: str, details: Optional[Dict[str, Any]] = None):
    """输出测试日志"""
    logger.test(message, details)


# 格式化函数
def format_emotion_description(emotion: str) -> str:
    """获取情感描述"""
    emotion_descriptions = {
        "happy": "开心",
        "sad": "悲伤", 
        "angry": "愤怒",
        "excited": "兴奋",
        "calm": "平静",
        "anxious": "焦虑",
        "neutral": "中性"
    }
    return emotion_descriptions.get(emotion, "未知情感")


def format_touch_zone_name(touch_zone: int) -> str:
    """获取抚摸区域名称"""
    touch_zones = {
        0: "头部",
        1: "背后", 
        2: "胸口"
    }
    return touch_zones.get(touch_zone, "未知区域")


def format_file_info(file_paths: Dict[str, str]) -> Dict[str, str]:
    """格式化文件信息"""
    return {
        "audio": file_paths.get('audio', '无'),
        "image": file_paths.get('image', '无'),
        "video": file_paths.get('video', '无')
    }


def format_interaction_details(robot_id: str, user_input: str, session_id: str, 
                            touch_zone: int, file_paths: Dict[str, str]) -> Dict[str, Any]:
    """格式化交互详情"""
    return {
        "robot_id": robot_id,
        "user_input": user_input,
        "session_id": session_id,
        "touch_zone": f"{touch_zone} ({format_touch_zone_name(touch_zone)})",
        "files": format_file_info(file_paths)
    } 