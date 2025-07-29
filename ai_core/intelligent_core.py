"""Module orchestrating all AI submodules.

文件结构：

```
UserInput       -> 数据类
IntelligentCore -> 调度情绪识别和对话生成
```
"""

from dataclasses import dataclass
from typing import Optional

from .dialogue_engine import DialogueEngine
from .emotion_perception import (
    EmotionPerception,
    DEFAULT_AUDIO_PATH,
    DEFAULT_IMAGE_PATH,
)


@dataclass
class UserInput:
    """Container for user-provided input paths and text.

    用户提供的语音、图像路径及文本内容。
    """
    audio_path: str = DEFAULT_AUDIO_PATH  # default demo audio 文件路径
    image_path: str = DEFAULT_IMAGE_PATH  # default demo image 图片路径
    text: str = ""                 # user input text 用户文本内容
    user_id: str = "unknown"       # 通过声纹识别得到的身份标识
    touched: bool = False          # 是否存在抚摸传感器交互


class IntelligentCore:
    """Main controller orchestrating submodules.

    整体调度各子模块的核心控制器。
    """

    def __init__(
        self,
        dialogue: Optional[DialogueEngine] = None,
        emotion: Optional[EmotionPerception] = None,
    ) -> None:
        """Initialize dialogue and emotion modules.

        初始化对话与情绪识别模块。

        Parameters
        ----------
        dialogue: DialogueEngine, optional
            Custom dialogue engine. 默认为 :class:`DialogueEngine`。
        emotion: EmotionPerception, optional
            Emotion perception module. 默认为 :class:`EmotionPerception`。
        """
        self.dialogue = dialogue or DialogueEngine()         # 对话系统
        self.emotion = emotion or EmotionPerception()        # 情绪识别系统

    def process(self, user: UserInput) -> str:
        """Process user input and generate a response.

        处理用户输入并生成回应。

        Parameters
        ----------
        user: UserInput
            Container holding audio path, image path and text. If omitted,
            defaults defined in :class:`UserInput` are used.
        """
        emotion_state = self.emotion.perceive(user.audio_path, user.image_path)  # 情绪识别
        mood = emotion_state.overall()  # 综合情绪结果
        user_id = self.emotion.recognize_identity(user.audio_path)  # 声纹识别身份
        user.user_id = user_id
        from . import global_state
        global_state.increment()  # 更新全局交互计数
        response = self.dialogue.generate_response(
            user.text,
            mood_tag=mood,
            user_id=user_id,
            touched=user.touched,
        )  # 生成回复
        return response
