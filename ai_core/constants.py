"""Common constants for the Companion Robot Intelligent Brain.

这个文件集中定义系统使用的常量，便于统一管理。"""

import os

# Absolute path to the project root 用于生成示例文件的绝对路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Default file paths for demos 默认的示例文件路径
DEFAULT_AUDIO_PATH = os.path.join(BASE_DIR, "..", "voice.wav")
DEFAULT_IMAGE_PATH = os.path.join(BASE_DIR, "..", "face.png")

# Default service endpoints 服务地址
DEFAULT_TTS_URL = os.environ.get("TTS_URL", "https://tts.szc.com")
DEFAULT_ASR_URL = os.environ.get("ASR_URL", "https://asr.szc.com")
DEFAULT_LLM_URL = os.environ.get("LLM_URL", "https://llm.szc.com")
DEFAULT_VOICEPRINT_URL = os.environ.get("VOICEPRINT_URL", "https://voiceprint.szc.com")
# Data storage service endpoints 数据存取服务
DEFAULT_MEMORY_SAVE_URL = os.environ.get(
    "MEMORY_SAVE_URL", "https://memory-save.szc.com"
)
DEFAULT_MEMORY_QUERY_URL = os.environ.get(
    "MEMORY_QUERY_URL", "https://memory-query.szc.com"
)

# Local fallback file when remote memory service is unavailable
# 远程记忆服务不可用时使用的本地备份文件
LOCAL_MEMORY_PATH = os.path.join(BASE_DIR, "..", "memory_backup.json")
# SQLite database path for persistent memory storage
# 用于持久化记忆的 SQLite 数据库文件
MEMORY_DB_PATH = os.path.join(BASE_DIR, "..", "memory.db")

# Global state persistence file 全局状态持久化文件
STATE_FILE = os.path.join(BASE_DIR, "..", "state.json")


# Growth stage default 默认成长阶段
DEFAULT_GROWTH_STAGE = "enlighten"

# Initial personality vector with extraversion 为外向性的人格向量
# OCEAN 模型五个维度依次为：开放性、责任心、外向性、宜人性、神经质
OCEAN_TRAITS = ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]
DEFAULT_PERSONALITY_VECTOR = [0.0, 0.0, 1.0, 0.0, 0.0]

# Initial global metric values 全局统计初始值
INITIAL_INTERACTIONS = 0
INITIAL_AUDIO_SECONDS = 0.0

# Growth stage threshold parameters 语言成长阶段阈值
# 每个阶段解锁需要达到的最小天数、交互次数以及语音时长（秒）
STAGE_THRESHOLDS = {
    "sprout": {"days": 3, "interactions": 5, "audio_seconds": 60},
    "enlighten": {"days": 10, "interactions": 20, "audio_seconds": 300},
    "resonate": {"days": 30, "interactions": 50, "audio_seconds": 900},
    # The awaken stage requires roughly twice the data of resonate
    "awaken": {"days": 45, "interactions": 75, "audio_seconds": 1500},
}

# Order of growth stages 成长阶段顺序
STAGE_ORDER = ["sprout", "enlighten", "resonate", "awaken"]

# Logging level 日志级别
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

# Allowed robot IDs 允许的机器人编号列表
ROBOT_ID_WHITELIST = ["robotA", "robotB"]

# Default thresholds for audio emotion recognition 音频情绪判断阈值
DEFAULT_RMS_ANGRY = 5000
DEFAULT_RMS_CALM = 1000

# Whether to use a multimodal model for emotion recognition
# 是否启用多模态模型进行情绪识别
DEFAULT_USE_MODEL = False

# Word lists used for simple text emotion detection
# 文本情绪检测的正负词表
POSITIVE_WORDS = ["happy", "great", "love", "good", "excited"]
NEGATIVE_WORDS = ["angry", "hate", "bad", "sad", "upset"]

# Standard emotion categories 行业通用情绪分类
EMOTION_STATES = [
    "neutral",       # 中性
    "happy",         # 开心
    "sad",           # 难过
    "angry",         # 生气
    "fear",          # 恐惧
    "surprise",      # 惊讶
    "disgust",       # 厌恶
    "calm",          # 平静
    "excited",       # 兴奋
    "tired",         # 疲惫
    "bored",         # 无聊
    "confused",      # 困惑
    "shy",           # 害羞
]

# LLM prompt template for emotion recognition
# 情绪识别的大模型提示模板
EMOTION_PROMPT_TEMPLATE = (
    "Identify the user's emotion from this text using one of the following tags: "
    "{options}. Text: '{text}'"
)

# Prompt template for multimodal emotion recognition
# 多模态情绪识别提示词模板
MULTI_MODAL_EMOTION_PROMPT = (
    "Identify the user's emotion from the given audio and image using one of the"
    " following tags: {options}. Audio file: {audio}. Image file: {image}. Text:"
    " '{text}'"
)

# Facial animation mapping for each mood 表情动画对应
FACE_ANIMATION_MAP = {
    "happy": (
        "微笑+眨眼+眼神上扬",
        "亮眼色彩、头部轻摆、手臂小幅打开",
    ),
    "confused": (
        "斜视+眼神聚焦",
        "停顿、轻微侧头、眼睛左右快速移动",
    ),
    "sad": (
        "眼角下垂+闭眼",
        "低亮度、轻微低头、手臂收回",
    ),
    "shy": (
        "偏头+眼神回避",
        "面部红晕特效、语音柔化、小动作微幅震颤",
    ),
    "excited": (
        "眼神放大+频繁眨眼",
        "快速摆头、双手前伸动作",
    ),
    "surprised": (
        "抬头张眼",
        "头部抬起，双手急速抬高",
    ),
}

# Motion mapping for body actions 动作映射
ACTION_MAP = {
    "happy": "nod±15°|sway±10°|hands_up10°",
    "confused": "tilt_oscillate±10°|gaze_switch|hands_still",
    "sad": "head_down_slow-15°|arms_arc_in",
    "surprised": "head_up_eyes_wide|hands_raise>25°",
    "shy": "idle_tremble",
    "excited": "fast_head_shake|hands_forward",
}

# Prompt templates for the large language model 大模型提示模板
STAGE_LLM_PROMPTS = {
    "sprout": "You are in the sprout stage. Reply with babbling sounds.",
    "enlighten": "You are in the enlighten stage. Imitate simple greetings like 'hello'.",
    "resonate": "You are in the resonate stage. Respond with caring short sentences and simple questions.",
    "awaken": "You are in the awaken stage. Use memories to give proactive suggestions.",
}

# 中文版本的大模型提示词
STAGE_LLM_PROMPTS_CN = {
    "sprout": "你正处于萌芽期，用咿呀声和简单动作回应。",
    "enlighten": "你已进入启蒙期，可以模仿并回答如\"你好\"等简短问候。",
    "resonate": "你已进入共鸣期，用关心的短句和简单问题交流。",
    "awaken": "你处于觉醒期，根据记忆主动提出建议并互动。",
}

# Personality trait prompts in English and Chinese 人格特质提示
OCEAN_LLM_PROMPTS = {
    "openness": "curious",
    "conscientiousness": "reliable",
    "extraversion": "outgoing",
    "agreeableness": "kind",
    "neuroticism": "sensitive",
}

OCEAN_LLM_PROMPTS_CN = {
    "openness": "好奇",
    "conscientiousness": "可靠",
    "extraversion": "外向",
    "agreeableness": "友善",
    "neuroticism": "敏感",
}

# Touch zone prompt mapping 触摸区域提示
TOUCH_ZONE_PROMPTS = {
    0: "The user touched your head. (用户触摸了你的头部)",
    1: "The user stroked your back. (用户抚摸了你的后背)",
    2: "The user touched your chest. (用户触摸了你的前胸)",
}
