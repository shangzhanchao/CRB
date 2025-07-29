"""Personality evolution engine for AI companion."""


class PersonalityEngine:
    """OCEAN personality growth engine with momentum decay.

    OCEAN 人格成长引擎，使用动量衰减机制平滑更新。
    """

    def __init__(self, momentum: float = 0.9):
        """Initialize the personality vector and settings.

        初始化五维人格向量和相关配置。
        """
        # OCEAN: Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism
        # OCEAN：开放性、责任心、外向性、宜人性、神经质
        self.vector = [0.0] * 5
        self.momentum = momentum
        # simple behavior map for demo purposes
        # 简单的行为标签映射表，用于示例
        self.behavior_map = {
            "praise": [0.1, 0.05, 0.1, 0.05, -0.05],
            "criticism": [-0.1, -0.05, -0.1, -0.05, 0.1],
        }

    def update(self, behavior_tag: str) -> None:
        """Update personality vector based on behavior tag.

        根据行为标签更新人格向量。
        """
        delta = self.behavior_map.get(behavior_tag, [0.0] * 5)
        self.vector = [
            self.momentum * v + (1 - self.momentum) * d
            for v, d in zip(self.vector, delta)
        ]

    def get_personality_style(self) -> str:
        """Return a simple language tone based on current personality.

        根据当前的人格向量返回语言风格。
        """
        extroversion = self.vector[2]
        if extroversion > 0.5:
            # 高外向性 -> 热情
            return "enthusiastic"
        if extroversion < -0.5:
            # 低外向性 -> 冷淡
            return "cold"
        return "neutral"
