"""Module orchestrating all AI submodules.

文件结构:

```
UserInput       -> 数据类
IntelligentCore -> 调度情绪识别和对话生成
```

The central brain receives **audio**, **touch** and **image** signals then
passes them through emotion recognition, memory retrieval and personality
growth to produce spoken replies, actions and facial expressions.
中央大脑接收语音、触摸和图像信息后，依次完成情绪识别、记忆查询、
人格成长，最终输出语音、动作与表情。
"""

from dataclasses import dataclass
from typing import Optional, Tuple
import logging

from .dialogue_engine import DialogueEngine, DialogueResponse
from .emotion_perception import EmotionPerception
from .constants import (
    DEFAULT_AUDIO_PATH,
    DEFAULT_IMAGE_PATH,
    LOG_LEVEL,
)

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)


@dataclass
class UserInput:
    """Container for user-provided input paths and text.

    用户提供的语音、图像路径及文本内容。除 ``robot_id`` 外均可为空。
    """

    audio_path: str | None = None  # 路径可为空
    image_path: str | None = None  # 图片路径可为空
    video_path: str | None = None  # 视频路径可为空
    text: str | None = None        # 文本内容可为空
    robot_id: str = ""             # 机器人编号 (必填)
    user_id: str | None = None     # 通过声纹识别得到的身份标识，可为空
    touched: bool = False          # 是否存在抚摸传感器交互
    touch_zone: int | None = None  # 触摸区域编号，可选


class IntelligentCore:
    """Main controller orchestrating submodules.

    整体调度各子模块的核心控制器。
    """

    def __init__(
        self,
        dialogue: Optional[DialogueEngine] = None,
        emotion: Optional[EmotionPerception] = None,
        asr_url: str | None = None,
        tts_url: str | None = None,
        llm_url: str | None = None,
        voiceprint_url: str | None = None,
    ) -> None:
        """Initialize dialogue and emotion modules.

        初始化对话与情绪识别模块。

        Parameters
        ----------
        dialogue: DialogueEngine, optional
            Custom dialogue engine. 默认为 :class:`DialogueEngine`。
        emotion: EmotionPerception, optional
            Emotion perception module. 默认为 :class:`EmotionPerception`。
        asr_url: str | None, optional
            Speech recognition service endpoint. ``None`` disables ASR.
        tts_url: str | None, optional
            Text to speech service endpoint. ``None`` disables TTS.
        llm_url: str | None, optional
            Large language model service endpoint.
        voiceprint_url: str | None, optional
            Speaker identification service endpoint.
        """
        self.dialogue = dialogue or DialogueEngine(llm_url=llm_url, tts_url=tts_url)  # 对话系统
        self.emotion = emotion or EmotionPerception(voiceprint_url=voiceprint_url)   # 情绪识别系统
        self.asr_url = asr_url

    def _resolve_paths(self, user: UserInput) -> Tuple[str, str]:
        """Return audio and image paths with fallbacks."""
        audio = user.audio_path or DEFAULT_AUDIO_PATH
        image = user.image_path or DEFAULT_IMAGE_PATH
        return audio, image

    def _ensure_text(self, user: UserInput, audio_path: str) -> None:
        """Fill ``user.text`` by ASR or empty string when missing."""
        if user.text:
            return
        if self.asr_url:
            from .service_clients import call_asr

            user.text = call_asr(audio_path, self.asr_url)
            logger.debug("ASR result: %s", user.text)
        else:
            user.text = ""
            logger.debug("No text input; defaulting to empty string")

    def _perceive(self, audio_path: str, image_or_video: str) -> Tuple[str, str]:
        """Return (mood, user_id) from multimodal perception."""
        emotion_state = self.emotion.perceive(audio_path, image_or_video)
        mood = emotion_state.overall()
        user_id = self.emotion.recognize_identity(audio_path)
        return mood, user_id

    def process(self, user: UserInput) -> DialogueResponse:
        """Process user input through the full pipeline.

        处理用户输入，按“语音 → 情绪识别 → 模型反馈 → 性格成长 → \
        对话生成”的流程返回结果。

        Parameters
        ----------
        user: UserInput
            Container holding audio path, image path, text and touch
            information. If omitted, defaults defined in
            :class:`UserInput` are used.
        """
        logger.info("Processing input for robot %s from %s", user.robot_id, user.user_id or "unknown")
        from . import global_state
        if not global_state.is_robot_allowed(user.robot_id):
            raise ValueError(f"Robot {user.robot_id} is not authorised")
        # Fill optional paths with defaults 用默认值填充可选路径
        audio_path, image_path = self._resolve_paths(user)
        # 1. ensure text content from ASR if necessary
        self._ensure_text(user, audio_path)

        # 2. emotion & identity perception
        img_or_video = user.video_path or image_path
        mood, user_id = self._perceive(audio_path, img_or_video)
        if not user_id or user_id == "unknown":
            # 声纹无法识别时创建新的访客身份
            user_id = f"guest_{global_state.INTERACTION_COUNT + 1}"
        logger.debug("Emotion: %s, user_id: %s", mood, user_id)
        user.user_id = user_id

        # 3. update global stats
        global_state.increment()  # 更新全局交互计数
        global_state.add_audio_duration(audio_path)  # 累加语音时长

        # 4. dialogue generation based on personality and memory
        response = self.dialogue.generate_response(
            user.text,
            mood_tag=mood,
            user_id=user_id,
            touched=user.touched,
            touch_zone=user.touch_zone,
        )  # 生成回复
        logger.info("Response text: %s", response.text)

        # response contains text, action, expression and optional audio URL
        return response
