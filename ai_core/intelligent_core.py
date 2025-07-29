from dataclasses import dataclass
from typing import Optional

from .dialogue_engine import DialogueEngine
from .emotion_perception import EmotionPerception


@dataclass
class UserInput:
    """Container for user-provided input paths and text.

    用户提供的语音、图像路径及文本内容。
    """
    audio_path: str
    image_path: str
    text: str


class IntelligentCore:
    """Main controller orchestrating submodules.

    整体调度各子模块的核心控制器。
    """

    def __init__(self):
        """Initialize dialogue and emotion modules.

        初始化对话与情绪识别模块。
        """
        self.dialogue = DialogueEngine()
        self.emotion = EmotionPerception()

    def process(self, user: UserInput) -> str:
        """Process user input and generate a response.

        处理用户输入并生成回应。
        """
        emotion_state = self.emotion.perceive(user.audio_path, user.image_path)
        mood = emotion_state.overall()
        response = self.dialogue.generate_response(user.text, mood_tag=mood)
        return response
