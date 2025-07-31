"""Emotion perception module.

Combines voice, face and text analysis to derive the user's mood.
情绪感知模块：综合语音、图像与文本信息判断用户当前的情绪状态。

File structure 文件结构：

```
EmotionState      -> 数据类，保存音频和图像情绪
EmotionPerception -> 识别语音与图像情绪并融合
```

Standard emotion tags include: happy, sad, angry, fear, surprise, disgust,
calm, excited, tired, bored, confused, shy and neutral.
"""

import os
import wave
import logging
from math import sqrt
from array import array
from dataclasses import dataclass
from collections import Counter
from typing import Optional

try:  # optional deep models
    from speechbrain.pretrained import EncoderClassifier  # type: ignore
except Exception:  # pragma: no cover - library missing
    EncoderClassifier = None

try:
    from fer import FER  # type: ignore
except Exception:  # pragma: no cover - library missing
    FER = None

from .semantic_memory import SemanticMemory
from .personality_engine import PersonalityEngine
from .service_api import call_llm


def calculate_rms(frames: bytes, sampwidth: int) -> float:
    """Return RMS amplitude of raw audio frames.

    计算原始音频帧的均方根幅值，兼容不再提供 ``audioop`` 模块的环境。

    Parameters
    ----------
    frames: bytes
        Raw audio data. 原始音频数据
    sampwidth: int
        Bytes per sample. 每个采样点的字节数
    """
    if not frames:
        return 0.0
    try:
        import numpy as np  # type: ignore

        dtype = {1: np.int8, 2: np.int16, 4: np.int32}.get(sampwidth, np.int16)
        data = np.frombuffer(frames, dtype=dtype).astype(np.float64)
        return float(np.sqrt(np.mean(data ** 2)))
    except Exception:  # pragma: no cover - numpy may be missing
        # Fallback using array module
        fmt = {1: 'b', 2: 'h', 4: 'i'}.get(sampwidth, 'h')
        arr = array(fmt)
        arr.frombytes(frames)
        squares = (sample * sample for sample in arr)
        mean_sq = sum(squares) / len(arr)
        return sqrt(mean_sq)


@dataclass
class EmotionState:
    """Emotion results from multiple modalities.

    来自语音、文本和面部的情绪识别结果。有效值参考 ``EMOTION_STATES``。
    """

    from_voice: str
    from_face: str
    from_text: str = "neutral"
    from_memory: Optional[str] = None

    def overall(self, personality: Optional[PersonalityEngine] = None) -> str:
        """Fuse emotions from all modalities and personality.

        融合语音、文本、视觉以及人格信息得到最终情绪。"""

        votes = [self.from_voice, self.from_face]
        if self.from_text != "neutral":
            votes.append(self.from_text)
        if self.from_memory:
            votes.append(self.from_memory)

        cnt = Counter(votes)
        mood, _ = cnt.most_common(1)[0]

        if self.from_text != "neutral":
            mood = self.from_text

        if mood == "neutral" and personality is not None:
            ext = personality.get_vector()[2]
            if ext > 0.5:
                mood = "happy"
            elif ext < -0.5:
                mood = "sad"

        return mood


from .constants import (
    DEFAULT_AUDIO_PATH,
    DEFAULT_IMAGE_PATH,
    LOG_LEVEL,
    DEFAULT_RMS_ANGRY,
    DEFAULT_RMS_CALM,
    POSITIVE_WORDS,
    NEGATIVE_WORDS,
    EMOTION_STATES,
    EMOTION_PROMPT_TEMPLATE,
    MULTI_MODAL_EMOTION_PROMPT,
    DEFAULT_USE_MODEL,
)

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)


class EmotionPerception:
    """Multimodal emotion recognition system.

    简易多模态情绪识别系统示例，可输入音频、图像与文本并返回融合后的
    :class:`EmotionState` 数据结构。
    """

    def __init__(
        self,
        rms_angry: int = DEFAULT_RMS_ANGRY,
        rms_calm: int = DEFAULT_RMS_CALM,
        voiceprint_url: str | None = None,
        llm_url: str | None = None,
        memory: Optional[SemanticMemory] = None,
        personality: Optional[PersonalityEngine] = None,
        use_model: bool = DEFAULT_USE_MODEL,
    ) -> None:
        """Set up any required models.

        初始化情绪识别模型或资源。

        Parameters
        ----------
        rms_angry: int, optional
            Threshold RMS value above which audio is considered angry. Defaults
            to :data:`DEFAULT_RMS_ANGRY`.
            音频均方根超过该值则判断为 "angry"，默认值为
            :data:`DEFAULT_RMS_ANGRY`。
        rms_calm: int, optional
            Threshold RMS below which audio is considered calm. Defaults to
            :data:`DEFAULT_RMS_CALM`.
            音频均方根低于该值则判断为 "calm"，默认值为
            :data:`DEFAULT_RMS_CALM`。
        llm_url: str | None, optional
            LLM service used for intent-based emotion classification.
            大模型服务地址，用于根据文本意图识别情绪。
        memory: SemanticMemory | None, optional
            Memory system used to reference past moods.
            语义记忆模块，可用于读取用户先前的情绪。
        personality: PersonalityEngine | None, optional
            Personality engine adjusting neutral moods.
            人格引擎，可在情绪模糊时根据外向性等因素调整结果。
        use_model: bool, optional
            If ``True`` use a multimodal model to directly infer emotion; if
            ``False`` use simple voice and image heuristics.  Defaults to
            :data:`DEFAULT_USE_MODEL`.
        """
        self.rms_angry = rms_angry
        self.rms_calm = rms_calm
        self.voiceprint_url = voiceprint_url
        self.llm_url = llm_url
        self.memory = memory
        self.personality = personality
        self.use_model = use_model

        # Load optional deep models when requested
        self.speech_model = None
        self.face_model = None
        if self.use_model:
            if EncoderClassifier is not None:
                try:  # type: ignore
                    self.speech_model = EncoderClassifier.from_hparams(
                        source="speechbrain/emotion-recognition-wav2vec2-IEMOCAP",
                        savedir="pretrained_models/speech_emotion",
                    )
                except Exception as exc:  # pragma: no cover - download failure
                    logger.warning("Speech emotion model load failed: %s", exc)
                    self.speech_model = None
            if FER is not None:
                try:
                    self.face_model = FER()
                except Exception as exc:  # pragma: no cover
                    logger.warning("Face model load failed: %s", exc)
                    self.face_model = None

    def recognize_identity(self, audio_path: str = DEFAULT_AUDIO_PATH) -> str:
        """Recognize speaker identity from voice.

        根据音频文件或远程声纹服务识别说话者身份。
        """
        logger.debug("Recognizing identity from %s", audio_path)
        if self.voiceprint_url:
            from .service_api import call_voiceprint

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
        if self.use_model and self.speech_model is not None:
            try:
                out_prob, score, index, text_lab = self.speech_model.classify_file(audio_path)  # type: ignore
                if text_lab:
                    return text_lab[0].lower()
            except Exception as exc:  # pragma: no cover
                logger.warning("Speech model failed: %s", exc)
        try:
            with wave.open(audio_path, "rb") as wf:
                frames = wf.readframes(wf.getnframes())
                rms = calculate_rms(frames, wf.getsampwidth())
            if rms > self.rms_angry:
                return "angry"
            if rms < self.rms_calm:
                return "calm"
        except Exception:
            pass  # file missing or unreadable 文件缺失或无法读取
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
        if self.use_model and self.face_model is not None:
            try:
                import cv2  # type: ignore
                img = cv2.imread(image_path)
                if img is not None:
                    emotion, score = self.face_model.top_emotion(img)  # type: ignore
                    if emotion:
                        return emotion.lower()
            except Exception as exc:  # pragma: no cover
                logger.warning("Face model failed: %s", exc)
        name = os.path.basename(image_path).lower()
        if "angry" in name:
            return "angry"
        if "happy" in name or "smile" in name:
            return "happy"
        return "neutral"

    def recognize_from_text(self, text: str) -> str:
        """Infer emotion from user text with optional LLM analysis.

        通过大模型或词表从用户文本推测情绪。
        """
        logger.debug("Recognizing emotion from text: %s", text)
        txt = text.strip()
        if not txt:
            return "neutral"
        if self.llm_url:
            prompt = EMOTION_PROMPT_TEMPLATE.format(
                options=", ".join(EMOTION_STATES), text=txt
            )
            llm_out = call_llm(prompt, self.llm_url).strip().lower()
            if llm_out in EMOTION_STATES:
                return llm_out
        text_lower = txt.lower()
        if any(w in text_lower for w in NEGATIVE_WORDS):
            return "angry"
        if any(w in text_lower for w in POSITIVE_WORDS):
            return "happy"
        return "neutral"

    def perceive(
        self,
        audio_path: str = DEFAULT_AUDIO_PATH,
        image_path: str = DEFAULT_IMAGE_PATH,
        text: str = "",
        user_id: str | None = None,
    ) -> EmotionState:
        """Perceive emotion from inputs using configured strategy.

        根据 ``use_model`` 选择简易融合或多模态模型来识别情绪。
        """

        if self.use_model:
            return self._perceive_model(audio_path, image_path, text, user_id)
        return self._perceive_simple(audio_path, image_path, text, user_id)

    def _perceive_simple(
        self,
        audio_path: str,
        image_path: str,
        text: str,
        user_id: str | None,
    ) -> EmotionState:
        """Simple heuristic fusion of voice and image emotions."""

        logger.info(
            "Perceiving emotion (simple) from %s and %s with text '%s'",
            audio_path,
            image_path,
            text,
        )
        voice_emotion = self.recognize_from_voice(audio_path)
        face_emotion = self.recognize_from_face(image_path)
        text_emotion = self.recognize_from_text(text) if text else "neutral"
        memory_mood = self.memory.last_mood(user_id) if self.memory else None

        state = EmotionState(
            from_voice=voice_emotion,
            from_face=face_emotion,
            from_text=text_emotion,
            from_memory=memory_mood,
        )

        mood = state.overall(self.personality)
        logger.debug("Emotion perceived (simple): %s | final mood %s", state, mood)
        if self.memory is not None and user_id is not None:
            self.memory.add_memory(text, "", mood, user_id)
        return state

    def _perceive_model(
        self,
        audio_path: str,
        image_path: str,
        text: str,
        user_id: str | None,
    ) -> EmotionState:
        """Use an external multimodal model to infer emotion."""

        logger.info(
            "Perceiving emotion (model) from %s and %s with text '%s'",
            audio_path,
            image_path,
            text,
        )
        # Prefer local deep models when available
        if self.speech_model is not None or self.face_model is not None:
            voice_emotion = self.recognize_from_voice(audio_path)
            face_emotion = self.recognize_from_face(image_path)
            text_emotion = self.recognize_from_text(text)
            state = EmotionState(
                from_voice=voice_emotion,
                from_face=face_emotion,
                from_text=text_emotion,
                from_memory=self.memory.last_mood(user_id) if self.memory else None,
            )
            result = state.overall(self.personality)
            logger.debug("Emotion perceived via local models: %s", state)
        elif self.llm_url:
            prompt = MULTI_MODAL_EMOTION_PROMPT.format(
                options=", ".join(EMOTION_STATES),
                audio=audio_path,
                image=image_path,
                text=text,
            )
            result = call_llm(prompt, self.llm_url).strip().lower()
            if result not in EMOTION_STATES:
                logger.warning(
                    "Model returned unknown emotion '%s'; falling back to simple mode",
                    result,
                )
                return self._perceive_simple(audio_path, image_path, text, user_id)
            state = EmotionState(result, result, result)
        else:
            logger.warning("No model available; falling back to simple mode")
            return self._perceive_simple(audio_path, image_path, text, user_id)

        if self.memory is not None and user_id is not None:
            self.memory.add_memory(text, "", result, user_id)
        logger.debug("Emotion perceived (model): %s", state)
        return state
