"""Common constants for the Companion Robot Intelligent Brain.

这个文件集中定义系统使用的常量，便于统一管理。"""

import os

# Default file paths for demos 默认的示例文件路径
DEFAULT_AUDIO_PATH = "voice.wav"
DEFAULT_IMAGE_PATH = "face.png"

# Default service endpoints 服务地址
DEFAULT_TTS_URL = os.environ.get("TTS_URL", "https://tts.szc.com")
DEFAULT_ASR_URL = os.environ.get("ASR_URL", "https://asr.szc.com")
DEFAULT_LLM_URL = os.environ.get("LLM_URL", "https://llm.szc.com")
DEFAULT_VOICEPRINT_URL = os.environ.get("VOICEPRINT_URL", "https://voiceprint.szc.com")

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
}

# Logging level 日志级别
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

# Allowed robot IDs 允许的机器人编号列表
ROBOT_ID_WHITELIST = ["robotA", "robotB"]

# Default thresholds for audio emotion recognition 音频情绪判断阈值
DEFAULT_RMS_ANGRY = 5000
DEFAULT_RMS_CALM = 1000

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
