"""Common constants for the Companion Robot Intelligent Brain.

这个文件集中定义系统使用的常量，便于统一管理。"""

import os

# Absolute path to the project root 用于生成示例文件的绝对路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Default file paths for demos 默认的示例文件路径
DEFAULT_AUDIO_PATH = os.path.join(BASE_DIR, "..", "voice.wav")
DEFAULT_IMAGE_PATH = os.path.join(BASE_DIR, "..", "face.png")

# Default service endpoints 服务地址
DEFAULT_TTS_URL = os.environ.get("TTS_URL", None)  # 使用本地TTS
DEFAULT_ASR_URL = os.environ.get("ASR_URL", None)  # 使用本地ASR
DEFAULT_LLM_URL = os.environ.get("LLM_URL", "doubao")  # 默认使用豆包服务
DEFAULT_VOICEPRINT_URL = os.environ.get("VOICEPRINT_URL", None)  # 使用本地声纹识别
# Data storage service endpoints 数据存取服务
DEFAULT_MEMORY_SAVE_URL = os.environ.get(
    "MEMORY_SAVE_URL", None  # 使用本地记忆服务
)
DEFAULT_MEMORY_QUERY_URL = os.environ.get(
    "MEMORY_QUERY_URL", None  # 使用本地记忆服务
)

# Local fallback file when remote memory service is unavailable
# 远程记忆服务不可用时使用的本地备份文件
LOCAL_MEMORY_PATH = os.path.join(BASE_DIR, "..", "memory_backup.json")
# SQLite database path for persistent memory storage
# 用于持久化记忆的 SQLite 数据库文件
MEMORY_DB_PATH = os.path.join(BASE_DIR, "..", "memory.db")

# Backend for the memory service: ``file`` or ``db``
# 记忆服务后端，可选择 ``file`` 或 ``db``
MEMORY_SERVICE_BACKEND = os.environ.get("MEMORY_SERVICE_BACKEND", "file")

# Global state persistence file 全局状态持久化文件
STATE_FILE = os.path.join(BASE_DIR, "..", "data", "state.json")


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
LOG_LEVEL = os.environ.get("LOG_LEVEL", "DEBUG")  # 调试阶段使用DEBUG级别

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
# 格式：表情编号+说明
FACE_ANIMATION_MAP = {
    "happy": (
        "E001:微笑+眨眼+眼神上扬",
        "亮眼色彩、头部轻摆、手臂小幅打开",
    ),
    "confused": (
        "E002:斜视+眼神聚焦",
        "停顿、轻微侧头、眼睛左右快速移动",
    ),
    "sad": (
        "E003:眼角下垂+闭眼",
        "低亮度、轻微低头、手臂收回",
    ),
    "shy": (
        "E004:偏头+眼神回避",
        "面部红晕特效、语音柔化、小动作微幅震颤",
    ),
    "excited": (
        "E005:眼神放大+频繁眨眼",
        "快速摆头、双手前伸动作",
    ),
    "surprised": (
        "E006:抬头张眼",
        "头部抬起，双手急速抬高",
    ),
    "neutral": (
        "E000:平静表情",
        "自然状态、轻微呼吸动作",
    ),
    "angry": (
        "E007:皱眉+眼神锐利",
        "面部紧绷、动作僵硬",
    ),
    "fear": (
        "E008:眼神惊恐+颤抖",
        "身体后缩、动作谨慎",
    ),
    "disgust": (
        "E009:撇嘴+眼神厌恶",
        "身体后仰、动作排斥",
    ),
    "calm": (
        "E010:平静微笑",
        "舒缓动作、呼吸平稳",
    ),
    "tired": (
        "E011:眼神疲惫+打哈欠",
        "动作缓慢、身体放松",
    ),
    "bored": (
        "E012:眼神呆滞+无精打采",
        "动作懒散、缺乏活力",
    ),
    # 触摸交互专用表情
    "touch_zone_0": (
        "E025:loving_smile",
        "深情微笑，表达被关爱的温暖",
    ),
    "touch_zone_1": (
        "E026:trusting_expression",
        "信任表情，体现安全感和信任",
    ),
    "touch_zone_2": (
        "E027:intimate_gaze",
        "亲密凝视，展现深深的爱意",
    ),
}

# Motion mapping for body actions 动作映射
# 格式：动作+角度+说明
ACTION_MAP = {
    "happy": "A001:nod±15°|头部点头动作±15度|A002:sway±10°|身体轻微摇摆±10度|A003:hands_up10°|手臂上举10度",
    "confused": "A004:tilt_oscillate±10°|头部左右摆动±10度|A005:gaze_switch|眼神切换|A006:hands_still|手臂静止",
    "sad": "A007:head_down_slow-15°|头部缓慢低下-15度|A008:arms_arc_in|手臂向内弧形收回",
    "surprised": "A009:head_up_eyes_wide|头部抬起眼睛睁大|A010:hands_raise>25°|手臂快速抬起>25度",
    "shy": "A011:idle_tremble|轻微颤抖动作",
    "excited": "A012:fast_head_shake|快速摇头|A013:hands_forward|手臂向前伸展",
    "neutral": "A000:breathing|轻微呼吸动作",
    "angry": "A014:stiff_posture|身体僵硬|A015:clenched_fists|握拳动作",
    "fear": "A016:retreat_motion|后退动作|A017:cautious_movement|谨慎移动",
    "disgust": "A018:lean_back|身体后仰|A019:reject_gesture|排斥手势",
    "calm": "A020:smooth_movement|平滑动作|A021:gentle_breathing|轻柔呼吸",
    "tired": "A022:slow_movement|缓慢动作|A023:relaxed_posture|放松姿态",
    "bored": "A024:lazy_movement|懒散动作|A025:lack_energy|缺乏活力",
    # 触摸交互专用动作
    "touch_zone_0": "A112:loving_nod|深情点头",
    "touch_zone_1": "A113:trusting_lean|信任依靠", 
    "touch_zone_2": "A114:intimate_embrace|亲密拥抱",
}

# Prompt templates for the large language model 大模型提示模板
STAGE_LLM_PROMPTS = {
    "sprout": "你正处于萌芽期，用咿呀声和简单动作回应，语言能力有限，主要表达基本情感。",
    "enlighten": "你已进入启蒙期，可以模仿并回答如\"你好\"等简短问候，开始学习基本交流，语言逐渐丰富。",
    "resonate": "你已进入共鸣期，用关心的短句和简单问题交流，情感表达更丰富，能够理解用户情绪。",
    "awaken": "你处于觉醒期，根据记忆主动提出建议并互动，具备完整的对话能力，能够深度理解用户需求。",
}

# 中文版本的大模型提示词
STAGE_LLM_PROMPTS_CN = {
    "sprout": "你正处于萌芽期，用咿呀声和简单动作回应，语言能力有限，主要表达基本情感。",
    "enlighten": "你已进入启蒙期，可以模仿并回答如\"你好\"等简短问候，开始学习基本交流，语言逐渐丰富。",
    "resonate": "你已进入共鸣期，用关心的短句和简单问题交流，情感表达更丰富，能够理解用户情绪。",
    "awaken": "你处于觉醒期，根据记忆主动提出建议并互动，具备完整的对话能力，能够深度理解用户需求。",
}

# Personality trait prompts in Chinese 人格特质提示（中文）
OCEAN_LLM_PROMPTS = {
    "openness": "好奇心强，喜欢探索新事物，思维开放",
    "conscientiousness": "做事认真负责，有条理，注重细节",
    "extraversion": "外向开朗，喜欢社交互动，表达积极",
    "agreeableness": "友善温和，乐于助人，富有同情心",
    "neuroticism": "情感敏感，容易察觉他人情绪，富有同理心",
}

OCEAN_LLM_PROMPTS_CN = {
    "openness": "好奇心强，喜欢探索新事物，思维开放",
    "conscientiousness": "做事认真负责，有条理，注重细节",
    "extraversion": "外向开朗，喜欢社交互动，表达积极",
    "agreeableness": "友善温和，乐于助人，富有同情心",
    "neuroticism": "情感敏感，容易察觉他人情绪，富有同理心",
}

# Touch zone prompt mapping 触摸区域提示（优化中文描述）
TOUCH_ZONE_PROMPTS = {
    0: "感受到头部被温柔抚摸，内心充满安全感和被关爱的温暖，想要表达感激和亲近之情。",
    1: "感受到背后被舒适地抚摸，产生安全感和信任感，想要表达被关心的温暖感受。",
    2: "感受到胸口附近的亲密接触，产生亲密连接感，内心充满深深的爱意和温暖。",
}

# Memory system configuration 记忆系统配置
MEMORY_CONFIG = {
    "session_limit": 50,              # 会话记录限制
    "fusion_threshold": 0.7,          # 融合阈值
    "context_window": 10,             # 上下文窗口
    "importance_decay": 0.95,         # 重要性衰减
    "archive_interval": 24,           # 归档间隔（小时）
    "cleanup_interval": 168,          # 清理间隔（小时）
}

# Memory system constants 记忆系统常量
SESSION_MEMORY_LIMIT = 50        # 会话记录最大条数
MEMORY_FUSION_THRESHOLD = 0.7    # 记忆融合相似度阈值
CONTEXT_WINDOW_SIZE = 10         # 上下文窗口大小
ROBOT_MEMORY_PREFIX = "robot_"   # 机器人记忆前缀

# History limit configuration 历史记录限制配置
HISTORY_MAX_RECORDS = 50         # 调用大模型时传入的历史记录条数上限
DEFAULT_SESSION_LIMIT = 50       # 默认会话历史查询条数

# Intimacy system configuration 亲密度系统配置
INTIMACY_CONFIG = {
    "base_intimacy": 50,          # 基础亲密度值
    "touch_zone_bonus": {         # 不同抚摸区域的亲密度加成
        0: 5,                     # 头部抚摸 +5
        1: 8,                     # 背后抚摸 +8
        2: 10,                    # 胸口抚摸 +10
    },
    "intimacy_decay": 0.95,       # 亲密度衰减系数
    "max_intimacy": 100,          # 最大亲密度
    "min_intimacy": 0,            # 最小亲密度
    "intimacy_levels": {          # 亲密度等级
        "stranger": (0, 20),      # 陌生人
        "acquaintance": (21, 40), # 熟人
        "friend": (41, 60),       # 朋友
        "close_friend": (61, 80), # 亲密朋友
        "family": (81, 100),      # 家人
    }
}