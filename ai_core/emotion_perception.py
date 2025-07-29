"""Emotion perception module.

文件结构：

```
EmotionState      -> 数据类，保存音频和图像情绪
EmotionPerception -> 识别语音与图像情绪并融合
```
"""

import os
import wave
import audioop
import logging
from dataclasses import dataclass


@dataclass
class EmotionState:
    """Emotion results from voice and face.

    来自语音和面部的情绪识别结果。
    """
    from_voice: str
    from_face: str

    def overall(self) -> str:
        """Fuse emotions from voice and face.

        融合语音与视觉的情绪结果。
        """
        if self.from_voice == self.from_face:
            return self.from_voice
        # naive fusion logic
        return self.from_voice or self.from_face


from .constants import DEFAULT_AUDIO_PATH, DEFAULT_IMAGE_PATH, LOG_LEVEL

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)


class EmotionPerception:
    """Placeholder multimodal emotion recognition system.

    简易多模态情绪识别系统示例。
    """

    def __init__(self, rms_angry: int = 5000, rms_calm: int = 1000, voiceprint_url: str | None = None) -> None:
        """Set up any required models.

        初始化情绪识别模型或资源。

        Parameters
        ----------
        rms_angry: int, optional
            Threshold RMS value above which audio is considered angry.
            音频均方根超过该值则判断为 "angry"，默认 5000。
        rms_calm: int, optional
            Threshold RMS below which audio is considered calm.
            音频均方根低于该值则判断为 "calm"，默认 1000。
        """
        self.rms_angry = rms_angry
        self.rms_calm = rms_calm
        self.voiceprint_url = voiceprint_url

    def recognize_identity(self, audio_path: str = DEFAULT_AUDIO_PATH) -> str:
        """Recognize speaker identity from voice.

        根据音频文件或远程声纹服务识别说话者身份。
        """
        logger.debug("Recognizing identity from %s", audio_path)
        if self.voiceprint_url:
            from .service_clients import call_voiceprint

            uid = call_voiceprint(audio_path, self.voiceprint_url)
            if uid:
                logger.info("Voiceprint matched user %s", uid)
                return uid
        name = os.path.basename(audio_path)
        user_id = os.path.splitext(name)[0]
        return user_id or "unknown"

    def recognize_from_voice(self, audio_path: str = DEFAULT_AUDIO_PATH) -> str:
        """Recognize emotion from audio.

        从语音音频中识别情绪（示例）。

        Parameters
        ----------
        audio_path: str, optional
            Path to an audio file. Defaults to :data:`DEFAULT_AUDIO_PATH` for
            demo purposes.  音频文件路径默认为
            :data:`DEFAULT_AUDIO_PATH`。
        """
        logger.debug("Recognizing emotion from voice file %s", audio_path)
        try:
            with wave.open(audio_path, "rb") as wf:
                frames = wf.readframes(wf.getnframes())
                rms = audioop.rms(frames, wf.getsampwidth())
            if rms > self.rms_angry:
                return "angry"
            if rms < self.rms_calm:
                return "calm"
        except Exception:
            # file missing or unreadable 文件缺失或无法读取
            pass
        name = os.path.basename(audio_path).lower()
        if "angry" in name:
            return "angry"
        if "happy" in name or "smile" in name:
            return "happy"
        return "neutral"

    def recognize_from_face(self, image_path: str = DEFAULT_IMAGE_PATH) -> str:
        """Recognize emotion from face image.

        从人脸图像识别情绪（示例）。

        Parameters
        ----------
        image_path: str, optional
            Path to a face image. Defaults to :data:`DEFAULT_IMAGE_PATH` to
            simplify testing.  人脸图片路径默认为
            :data:`DEFAULT_IMAGE_PATH`。
        """
        logger.debug("Recognizing emotion from face image %s", image_path)
        name = os.path.basename(image_path).lower()
        if "angry" in name:
            return "angry"
        if "happy" in name or "smile" in name:
            return "happy"
        return "neutral"

    def perceive(
        self,
        audio_path: str = DEFAULT_AUDIO_PATH,
        image_path: str = DEFAULT_IMAGE_PATH,
    ) -> EmotionState:
        """Perceive emotion from multimodal inputs.

        结合语音和视觉信息感知情绪。

        Parameters
        ----------
        audio_path: str, optional
            Voice recording path. :data:`DEFAULT_AUDIO_PATH` by default for
            quick demos.
        image_path: str, optional
            Face image path. Default :data:`DEFAULT_IMAGE_PATH`.
        """
        logger.info("Perceiving emotion from %s and %s", audio_path, image_path)
        voice_emotion = self.recognize_from_voice(audio_path)
        face_emotion = self.recognize_from_face(image_path)
        state = EmotionState(from_voice=voice_emotion, from_face=face_emotion)
        logger.debug("Emotion perceived: %s", state)
        return state  # 返回融合后的情绪状态
