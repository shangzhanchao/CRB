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

from .enhanced_dialogue_engine import EnhancedDialogueEngine, DialogueResponse
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
    session_id: str | None = None  # 会话ID，用于上下文连续性


class IntelligentCore:
    """Main controller orchestrating submodules.

    整体调度各子模块的核心控制器。
    """

    def __init__(
        self,
        robot_id: str = "robotA",
        dialogue: Optional[EnhancedDialogueEngine] = None,
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
        robot_id: str
            机器人ID
        dialogue: EnhancedDialogueEngine, optional
            Custom dialogue engine. 默认为 :class:`EnhancedDialogueEngine`。
        emotion: EmotionPerception, optional
            Emotion perception module. 默认为 :class:`EmotionPerception`。
        asr_url: str | None, optional
            Speech recognition service endpoint. ``None`` disables ASR.
        tts_url: str | None, optional
            Text to speech service endpoint.
        llm_url: str | None, optional
            Large language model service endpoint.
        voiceprint_url: str | None, optional
            Speaker identification service endpoint.
        """
        # 如果没有提供llm_url，使用默认值
        if llm_url is None:
            from .constants import DEFAULT_LLM_URL
            llm_url = DEFAULT_LLM_URL
        
        self.robot_id = robot_id
        self.dialogue = dialogue or EnhancedDialogueEngine(
            robot_id=robot_id,
            llm_url=llm_url, 
            tts_url=tts_url
        )  # 增强对话系统
        self.emotion = emotion or EmotionPerception(
            voiceprint_url=voiceprint_url,
            llm_url=llm_url,
            memory=self.dialogue.memory,
            personality=self.dialogue.personality,
        )   # 情绪识别系统
        self.asr_url = asr_url
        
        logger.info(f"🔧 智能核心初始化完成")
        logger.info(f"   🤖 机器人ID: {robot_id}")
        logger.info(f"   💬 对话引擎: {'已连接' if dialogue else '新建'}")
        logger.info(f"   😊 情绪识别: {'已连接' if emotion else '新建'}")
        logger.info(f"   🎤 ASR服务: {asr_url or '未配置'}")
        logger.info(f"   🔊 TTS服务: {tts_url or '未配置'}")
        logger.info(f"   🤖 LLM服务: {llm_url or '未配置'}")

    def _resolve_paths(self, user: UserInput) -> Tuple[str, str]:
        """Return audio and image paths with fallbacks.

        返回解析第一位可选路径，如不提供则使用默认文件。
        """
        audio_path = user.audio_path or DEFAULT_AUDIO_PATH
        image_or_video = user.image_path or user.video_path or DEFAULT_IMAGE_PATH
        return audio_path, image_or_video

    def _ensure_text(self, user: UserInput, audio_path: str) -> None:
        """Ensure user.text is populated, using ASR if needed.

        确保用户文本已填充，如需要则使用ASR。
        """
        if not user.text and self.asr_url:
            try:
                from .service_api import call_asr
                user.text = call_asr(audio_path, self.asr_url)
                logger.info(f"ASR识别结果: {user.text}")
            except Exception as e:
                logger.error(f"ASR调用失败: {e}")
                user.text = ""

    def _perceive(self, audio_path: str, image_or_video: str, text: str) -> Tuple[str, str]:
        """Perceive emotion from multimodal input.

        从多模态输入感知情绪。
        """
        try:
            mood_tag, user_id = self.emotion.perceive_emotion(
                audio_path, image_or_video, text
            )
            logger.info(f"情绪识别结果: {mood_tag}, 用户ID: {user_id}")
            return mood_tag, user_id
        except Exception as e:
            logger.error(f"情绪识别失败: {e}")
            return "neutral", "unknown"

    def process(self, user: UserInput) -> DialogueResponse:
        """Process user input and generate response.

        处理用户输入并生成回复。

        Parameters
        ----------
        user: UserInput
            User input data container.

        Returns
        -------
        DialogueResponse
            Generated response with text, audio, actions and expressions.
        """
        logger.info(f"🎯 开始处理用户输入 - 机器人: {user.robot_id}")
        logger.info(f"   📝 文本: {user.text}")
        logger.info(f"   🎵 音频: {user.audio_path}")
        logger.info(f"   🖼️ 图像: {user.image_path}")
        logger.info(f"   🎬 视频: {user.video_path}")
        logger.info(f"   🤗 触摸区域: {user.touch_zone}")
        logger.info(f"   🆔 会话ID: {user.session_id}")

        # 1. 解析路径
        audio_path, image_or_video = self._resolve_paths(user)
        
        # 2. 确保文本内容
        self._ensure_text(user, audio_path)
        
        # 3. 情绪感知
        mood_tag, user_id = self._perceive(audio_path, image_or_video, user.text or "")
        
        # 4. 生成回复
        touched = user.touch_zone is not None
        
        response = self.dialogue.generate_response(
            user_text=user.text or "",
            mood_tag=mood_tag,
            user_id=user_id,
            touched=touched,
            touch_zone=user.touch_zone,
            session_id=user.session_id,
        )
        
        logger.info(f"✅ 处理完成")
        logger.info(f"   📝 回复文本: {response.text}")
        logger.info(f"   🎵 音频URL: {response.audio}")
        logger.info(f"   🎭 表情: {response.expression}")
        logger.info(f"   🤸 动作: {response.action}")
        logger.info(f"   🆔 会话ID: {response.session_id}")
        logger.info(f"   🪟 上下文摘要: {response.context_summary}")
        logger.info(f"   💾 记忆数量: {response.memory_count}")
        
        return response

    async def process_async(self, user: UserInput) -> DialogueResponse:
        """Process user input asynchronously.

        异步处理用户输入。

        Parameters
        ----------
        user: UserInput
            User input data container.

        Returns
        -------
        DialogueResponse
            Generated response with text, audio, actions and expressions.
        """
        # 在异步环境中运行同步处理
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.process, user)

    def start_session(self, session_id: Optional[str] = None) -> str:
        """开始新会话"""
        return self.dialogue.start_session(session_id)

    def get_memory_stats(self) -> dict:
        """获取记忆统计信息"""
        return self.dialogue.get_memory_stats()

    def clear_session_memory(self, session_id: Optional[str] = None) -> int:
        """清除会话记忆"""
        return self.dialogue.clear_session_memory(session_id)

    def close(self):
        """关闭智能核心"""
        if hasattr(self, 'dialogue'):
            self.dialogue.close()
        logger.info("🔒 智能核心已关闭")