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
import asyncio
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
    """Container for incoming interaction data.

    用户输入的数据容器，仅 ``robot_id`` 为必填，其余皆可为空。包含
    文本、音频、图像、视频及触摸区域编号共六项。"""

    audio_path: str | None = None  # 路径可为空
    image_path: str | None = None  # 图片路径可为空
    video_path: str | None = None  # 视频路径可为空
    text: str | None = None        # 文本内容可为空
    robot_id: str = ""             # 机器人编号 (必填)
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
        self.emotion = emotion or EmotionPerception(
            voiceprint_url=voiceprint_url,
            llm_url=llm_url,
            memory=self.dialogue.memory,
            personality=self.dialogue.personality,
        )   # 情绪识别系统
        self.asr_url = asr_url

    def _resolve_paths(self, user: UserInput) -> Tuple[str, str]:
        """Return audio and image paths with fallbacks.

        返回解析第一位可选路径，如不提供则使用默认文件。
        """
        audio = user.audio_path or DEFAULT_AUDIO_PATH
        image = user.image_path or DEFAULT_IMAGE_PATH
        return audio, image

    def _ensure_text(self, user: UserInput, audio_path: str) -> None:
        """Fill ``user.text`` by ASR or empty string when missing.

        当用户没有提供文本时，若指定 ASR 服务会自动识别语音，否则使用空字符代替。
        """
        if user.text:
            return
        if self.asr_url:
            from .service_api import call_asr

            user.text = call_asr(audio_path, self.asr_url)
            logger.debug("ASR result: %s", user.text)
        else:
            user.text = ""
            logger.debug("No text input; defaulting to empty string")

    def _perceive(self, audio_path: str, image_or_video: str, text: str) -> Tuple[str, str]:
        """Return (mood, user_id) from multimodal perception.

        输入音频、图像或视频以及文本，通过情绪识别系统返回情绪标签和认证的用户ID。
        """

        user_id = self.emotion.recognize_identity(audio_path)
        emotion_state = self.emotion.perceive(
            audio_path,
            image_or_video,
            text=text,
            user_id=user_id,
        )
        mood = emotion_state.overall(self.dialogue.personality)
        return mood, user_id

    def process(self, user: UserInput) -> DialogueResponse:
        """Process user input through the full pipeline.

        处理用户输入，按“语音 → 情绪识别 → 模型反馈 → 性格成长 → \
        对话生成”的流程返回 ``DialogueResponse``。

        Parameters
        ----------
        user: UserInput
            Input data including optional text, audio, image, video and touch
            zone. ``robot_id`` must be provided. Missing fields will use
            defaults from :class:`UserInput`.

        Returns
        -------
        DialogueResponse
            Structured reply containing non-empty ``text``, ``audio``,
            ``action`` and ``expression`` fields.
        """
        logger.info("Processing input for robot %s", user.robot_id)
        from . import global_state
        if not global_state.is_robot_allowed(user.robot_id):
            raise ValueError(
                f"Robot ID '{user.robot_id}' is not allowed. 请检查机器人编号是否在白名单内"
            )
        # Fill optional paths with defaults 用默认值填充可选路径
        audio_path, image_path = self._resolve_paths(user)
        # 1. ensure text content from ASR if necessary
        self._ensure_text(user, audio_path)

        # 2. emotion & identity perception
        img_or_video = user.video_path or image_path
        mood, user_id = self._perceive(audio_path, img_or_video, user.text)
        if not user_id or user_id == "unknown":
            # 声纹无法识别时创建新的访客身份
            user_id = f"guest_{global_state.INTERACTION_COUNT + 1}"
        logger.debug("Emotion: %s, user_id: %s", mood, user_id)

        # 3. update global stats
        global_state.increment()  # 更新全局交互计数
        global_state.add_audio_duration(audio_path)  # 累加语音时长

        # 4. dialogue generation based on personality and memory
        response = self.dialogue.generate_response(
            user.text,
            mood_tag=mood,
            user_id=user_id,
            touched=user.touch_zone is not None,
            touch_zone=user.touch_zone,
        )  # 生成回复
        logger.info("Response text: %s", response.text)

        # response contains text, action, expression and optional audio URL
        return response

    async def process_async(self, user: UserInput) -> DialogueResponse:
        """Asynchronous version using async service APIs."""

        logger.info("Async processing for robot %s", user.robot_id)
        from . import global_state

        if not global_state.is_robot_allowed(user.robot_id):
            raise ValueError(
                f"Robot ID '{user.robot_id}' is not allowed. 请检查机器人编号是否在白名单内"
            )
        audio_path, image_path = self._resolve_paths(user)
        if not user.text and self.asr_url:
            from .service_api import async_call_asr

            user.text = await async_call_asr(audio_path, self.asr_url)
        else:
            user.text = user.text or ""

        img_or_video = user.video_path or image_path
        mood, user_id = self._perceive(audio_path, img_or_video, user.text)
        if not user_id or user_id == "unknown":
            user_id = f"guest_{global_state.INTERACTION_COUNT + 1}"

        global_state.increment()
        global_state.add_audio_duration(audio_path)

        response = self.dialogue.generate_response(
            user.text,
            mood_tag=mood,
            user_id=user_id,
            touched=user.touch_zone is not None,
            touch_zone=user.touch_zone,
        )
        return response
