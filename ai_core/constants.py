"""Common constants for the Companion Robot Intelligent Brain.

這個文件集中定義系統使用的常量，便於統一管理。"""

import os

# Default file paths for demos 預設的示例文件路徑
DEFAULT_AUDIO_PATH = "voice.wav"
DEFAULT_IMAGE_PATH = "face.png"

# Default service endpoints 服務地址
DEFAULT_TTS_URL = os.environ.get("TTS_URL", "https://tts.szc.com")
DEFAULT_ASR_URL = os.environ.get("ASR_URL", "https://asr.szc.com")
DEFAULT_LLM_URL = os.environ.get("LLM_URL", "https://llm.szc.com")
DEFAULT_VOICEPRINT_URL = os.environ.get("VOICEPRINT_URL", "https://voiceprint.szc.com")

# Growth stage default 默認成長階段
DEFAULT_GROWTH_STAGE = "enlighten"

# Initial personality vector with extraversion 為外向性的人格向量
DEFAULT_PERSONALITY_VECTOR = [0.0, 0.0, 1.0, 0.0, 0.0]

# Initial global metric values 全局統計初始值
INITIAL_INTERACTIONS = 0
INITIAL_AUDIO_SECONDS = 0.0

# Logging level 日誌級別
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
