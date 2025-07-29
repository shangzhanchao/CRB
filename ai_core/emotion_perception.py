import os
import wave
import audioop
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


DEFAULT_AUDIO_PATH = "voice.wav"
DEFAULT_IMAGE_PATH = "face.png"


class EmotionPerception:
    """Placeholder multimodal emotion recognition system.

    简易多模态情绪识别系统示例。
    """

    def __init__(self, rms_angry: int = 5000, rms_calm: int = 1000) -> None:
        """Set up any required models.

        初始化情绪识别模型或资源。
        """
        self.rms_angry = rms_angry
        self.rms_calm = rms_calm

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
        try:
            with wave.open(audio_path, "rb") as wf:
                frames = wf.readframes(wf.getnframes())
                rms = audioop.rms(frames, wf.getsampwidth())
            if rms > self.rms_angry:
                return "angry"
            if rms < self.rms_calm:
                return "calm"
        except Exception:
            # file missing or unreadable
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
        voice_emotion = self.recognize_from_voice(audio_path)
        face_emotion = self.recognize_from_face(image_path)
        return EmotionState(from_voice=voice_emotion, from_face=face_emotion)
