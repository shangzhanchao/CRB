"""Personality evolution engine for AI companion.

该文件包含以下结构：

```
DEFAULT_BEHAVIOR_MAP -> 行为标签到 OCEAN 向量增量的映射
PersonalityEngine    -> 核心类，负责维护人格向量并依据行为更新
```

Module layout commentary helps new developers quickly understand how each
piece fits together.
"""


DEFAULT_BEHAVIOR_MAP = {
    "praise": [0.1, 0.05, 0.1, 0.05, -0.05],
    "criticism": [-0.1, -0.05, -0.1, -0.05, 0.1],
    "joke": [0.05, -0.05, 0.2, 0.1, -0.05],
    "support": [0.05, 0.1, 0.05, 0.1, -0.05],
    "touch": [0.05, 0.05, 0.1, 0.1, -0.05],  # 抚摸交互行为
}


class PersonalityEngine:
    """OCEAN personality growth engine with momentum decay.

    OCEAN 人格成长引擎，使用动量衰减机制平滑更新。
    """

    def __init__(
        self,
        momentum: float = 0.9,
        behavior_map: dict | None = None,
    ) -> None:
        """Initialize the personality vector and settings.

        初始化五维人格向量和相关配置。

        Parameters
        ----------
        momentum: float, optional
            Momentum decay factor controlling update smoothness. 默认为 ``0.9``
            表示更新时保持 90% 的历史状态。
        behavior_map: dict | None, optional
            Mapping from behavior tag to OCEAN vector deltas. 如未提供，
            默认使用 :data:`DEFAULT_BEHAVIOR_MAP`。
        """
        # OCEAN: Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism
        # OCEAN：开放性、责任心、外向性、宜人性、神经质
        self.vector = [0.0] * 5  # five-dimensional OCEAN trait vector 人格向量
        self.momentum = momentum  # 动量衰减因子
        # 行为标签映射表，可自定义传入
        self.behavior_map = behavior_map or DEFAULT_BEHAVIOR_MAP

    def update(self, behavior_tag: str = "neutral") -> None:
        """Update personality vector based on behavior tag.

        根据行为标签更新人格向量。

        Parameters
        ----------
        behavior_tag: str, optional
            Tag describing user behavior. Defaults to ``"neutral"`` when no
            specific behavior is supplied.  用户行为标签，默认值为
            ``"neutral"`` 时，不会对人格向量产生调整。
        """
        delta = self.behavior_map.get(behavior_tag, [0.0] * 5)
        # 使用动量衰减更新人格向量，确保变化平滑
        self.vector = [
            max(-1.0, min(1.0, self.momentum * v + (1 - self.momentum) * d))
            for v, d in zip(self.vector, delta)
        ]

    def get_personality_style(self) -> str:
        """Return a simple language tone based on current personality.

        根据当前的人格向量返回语言风格。
        """
        extroversion = self.vector[2]  # index 2 corresponds to Extraversion
        if extroversion > 0.5:
            # 高外向性 -> 热情
            return "enthusiastic"
        if extroversion < -0.5:
            # 低外向性 -> 冷淡
            return "cold"
        return "neutral"

    def get_vector(self):
        """Return the current OCEAN vector. 返回当前的人格向量。"""
        return list(self.vector)
