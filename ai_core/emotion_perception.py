"""Emotion perception module.

情绪识别模块，负责从多模态输入中识别用户情绪。
"""

import logging
from typing import Optional, Tuple

from .constants import LOG_LEVEL

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)


class EmotionPerception:
    """Emotion perception system.

    情绪识别系统，从音频、图像、视频和文本中识别用户情绪。
    """

    def __init__(
        self,
        voiceprint_url: str | None = None,
        llm_url: str | None = None,
        memory=None,
        personality=None,
    ) -> None:
        """Initialize emotion perception system.

        初始化情绪识别系统。

        Parameters
        ----------
        voiceprint_url: str | None, optional
            Voiceprint service endpoint.
        llm_url: str | None, optional
            Large language model service endpoint.
        memory: optional
            Memory system for context.
        personality: optional
            Personality system for context.
        """
        self.voiceprint_url = voiceprint_url
        self.llm_url = llm_url
        self.memory = memory
        self.personality = personality
        
        logger.info(f"🔧 情绪识别系统初始化完成")
        logger.info(f"   🎤 声纹服务: {voiceprint_url or '未配置'}")
        logger.info(f"   🤖 LLM服务: {llm_url or '未配置'}")

    def recognize_identity(self, audio_path: str) -> str:
        """Recognize user identity from audio.

        从音频中识别用户身份。

        Parameters
        ----------
        audio_path: str
            Path to audio file.

        Returns
        -------
        str
            User identifier.
        """
        # 简单的身份识别实现
        if self.voiceprint_url:
            try:
                from .service_api import call_voiceprint
                user_id = call_voiceprint(audio_path, self.voiceprint_url)
                logger.info(f"🎤 声纹识别结果: {user_id}")
                return user_id
            except Exception as e:
                logger.error(f"❌ 声纹识别失败: {e}")
                return "unknown"
        else:
            return "unknown"

    def perceive_emotion(
        self, 
        audio_path: str, 
        image_or_video: str, 
        text: str
    ) -> Tuple[str, str]:
        """Perceive emotion from multimodal input.

        从多模态输入感知情绪。

        Parameters
        ----------
        audio_path: str
            Path to audio file.
        image_or_video: str
            Path to image or video file.
        text: str
            Text input.

        Returns
        -------
        Tuple[str, str]
            (mood_tag, user_id)
        """
        try:
            # 识别用户身份
            user_id = self.recognize_identity(audio_path)
            
            # 感知情绪
            emotion_state = self.perceive(
                audio_path, image_or_video, text, user_id
            )
            
            # 获取主导情绪
            mood = emotion_state.overall(self.personality) if self.personality else "neutral"
            
            logger.info(f"😊 情绪识别结果: {mood}, 用户ID: {user_id}")
            return mood, user_id
            
        except Exception as e:
            logger.error(f"❌ 情绪识别失败: {e}")
            return "neutral", "unknown"

    def perceive(
        self,
        audio_path: str,
        image_or_video: str,
        text: str = "",
        user_id: str = "unknown",
    ) -> "EmotionState":
        """Perceive emotion from multimodal input.

        从多模态输入感知情绪。

        Parameters
        ----------
        audio_path: str
            Path to audio file.
        image_or_video: str
            Path to image or video file.
        text: str, optional
            Text input.
        user_id: str, optional
            User identifier.

        Returns
        -------
        EmotionState
            Emotion state object.
        """
        # 创建情绪状态对象
        emotion_state = EmotionState()
        
        # 从文本中识别情绪
        if text:
            emotion_state.text_emotion = self._analyze_text_emotion(text)
        
        # 从音频中识别情绪
        if audio_path:
            emotion_state.audio_emotion = self._analyze_audio_emotion(audio_path)
        
        # 从图像/视频中识别情绪
        if image_or_video:
            emotion_state.visual_emotion = self._analyze_visual_emotion(image_or_video)
        
        # 综合情绪分析
        emotion_state.overall_emotion = self._combine_emotions(emotion_state)
        
        logger.info(f"😊 情绪感知完成:")
        logger.info(f"   📝 文本情绪: {emotion_state.text_emotion}")
        logger.info(f"   🎵 音频情绪: {emotion_state.audio_emotion}")
        logger.info(f"   🖼️ 视觉情绪: {emotion_state.visual_emotion}")
        logger.info(f"   🎯 综合情绪: {emotion_state.overall_emotion}")
        
        return emotion_state

    def _analyze_text_emotion(self, text: str) -> str:
        """Analyze emotion from text.

        从文本中分析情绪。

        Parameters
        ----------
        text: str
            Input text.

        Returns
        -------
        str
            Emotion tag.
        """
        # 简单的关键词匹配
        text_lower = text.lower()
        
        # 积极情绪关键词
        positive_keywords = ["开心", "高兴", "快乐", "兴奋", "愉快", "好", "棒", "赞", "喜欢", "爱"]
        for keyword in positive_keywords:
            if keyword in text_lower:
                return "happy"
        
        # 消极情绪关键词
        negative_keywords = ["难过", "伤心", "悲伤", "沮丧", "失望", "不好", "讨厌", "恨", "生气", "愤怒"]
        for keyword in negative_keywords:
            if keyword in text_lower:
                return "sad"
        
        # 惊讶情绪关键词
        surprise_keywords = ["惊讶", "震惊", "意外", "吃惊", "哇", "哦", "真的吗"]
        for keyword in surprise_keywords:
            if keyword in text_lower:
                return "surprised"
        
        # 愤怒情绪关键词
        anger_keywords = ["生气", "愤怒", "恼火", "烦躁", "讨厌", "恨"]
        for keyword in anger_keywords:
            if keyword in text_lower:
                return "angry"
        
        # 兴奋情绪关键词
        excited_keywords = ["激动", "兴奋", "热情", "振奋", "太棒了", "太好了"]
        for keyword in excited_keywords:
            if keyword in text_lower:
                return "excited"
        
        return "neutral"

    def _analyze_audio_emotion(self, audio_path: str) -> str:
        """Analyze emotion from audio.

        从音频中分析情绪。

        Parameters
        ----------
        audio_path: str
            Path to audio file.

        Returns
        -------
        str
            Emotion tag.
        """
        # 简单的音频情绪分析
        # 这里可以集成更复杂的音频分析库
        try:
            # 检查音频文件是否存在
            import os
            if os.path.exists(audio_path):
                # 基于文件大小的简单判断
                file_size = os.path.getsize(audio_path)
                if file_size > 10000:  # 大于10KB的音频可能包含更多信息
                    return "excited"
                else:
                    return "neutral"
            else:
                return "neutral"
        except Exception as e:
            logger.error(f"❌ 音频情绪分析失败: {e}")
            return "neutral"

    def _analyze_visual_emotion(self, image_or_video: str) -> str:
        """Analyze emotion from visual input.

        从视觉输入中分析情绪。

        Parameters
        ----------
        image_or_video: str
            Path to image or video file.

        Returns
        -------
        str
            Emotion tag.
        """
        # 简单的视觉情绪分析
        try:
            # 检查文件是否存在
            import os
            if os.path.exists(image_or_video):
                # 基于文件扩展名的简单判断
                file_ext = os.path.splitext(image_or_video)[1].lower()
                if file_ext in ['.jpg', '.jpeg', '.png', '.gif']:
                    return "happy"  # 图片通常表示积极情绪
                elif file_ext in ['.mp4', '.avi', '.mov', '.webm']:
                    return "excited"  # 视频通常表示兴奋情绪
                else:
                    return "neutral"
            else:
                return "neutral"
        except Exception as e:
            logger.error(f"❌ 视觉情绪分析失败: {e}")
            return "neutral"

    def _combine_emotions(self, emotion_state: "EmotionState") -> str:
        """Combine emotions from different modalities.

        融合不同模态的情绪。

        Parameters
        ----------
        emotion_state: EmotionState
            Emotion state object.

        Returns
        -------
        str
            Combined emotion tag.
        """
        emotions = []
        
        if emotion_state.text_emotion != "neutral":
            emotions.append(emotion_state.text_emotion)
        
        if emotion_state.audio_emotion != "neutral":
            emotions.append(emotion_state.audio_emotion)
        
        if emotion_state.visual_emotion != "neutral":
            emotions.append(emotion_state.visual_emotion)
        
        if not emotions:
            return "neutral"
        
        # 简单的情绪融合策略
        # 如果有多个情绪，选择第一个非中性情绪
        return emotions[0]


class EmotionState:
    """Emotion state container.

    情绪状态容器。
    """

    def __init__(self):
        """Initialize emotion state."""
        self.text_emotion = "neutral"
        self.audio_emotion = "neutral"
        self.visual_emotion = "neutral"
        self.overall_emotion = "neutral"

    def overall(self, personality=None) -> str:
        """Get overall emotion considering personality.

        考虑人格因素的综合情绪。

        Parameters
        ----------
        personality: optional
            Personality system.

        Returns
        -------
        str
            Overall emotion tag.
        """
        # 如果有情绪识别结果，使用它
        if self.overall_emotion != "neutral":
            return self.overall_emotion
        
        # 否则使用文本情绪
        return self.text_emotion