"""Personality evolution engine for the companion robot.

该文件包含以下结构：

```
DEFAULT_BEHAVIOR_MAP -> 行为标签到 OCEAN 向量增量的映射
PersonalityEngine    -> 核心类，负责维护人格向量并依据行为更新
```

Module layout commentary helps new developers quickly understand how each
piece fits together.
"""

import logging

from .constants import DEFAULT_PERSONALITY_VECTOR, LOG_LEVEL


#
# Mapping from behaviour tags to OCEAN deltas.
# 行为标签到 OCEAN 向量增量的映射表。
#
# Each list contains five numbers representing adjustments for
# ``[Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism]``.
# These increments are blended with the current personality vector using the
# momentum decay factor so personality shifts remain smooth.
#
DEFAULT_BEHAVIOR_MAP = {
    "praise": [0.1, 0.05, 0.1, 0.05, -0.05],       # 用户夸奖机器人
    "criticism": [-0.1, -0.05, -0.1, -0.05, 0.1],  # 用户批评机器人
    "joke": [0.05, -0.05, 0.2, 0.1, -0.05],        # 轻松幽默的互动
    "support": [0.05, 0.1, 0.05, 0.1, -0.05],      # 鼓励或支持
    "touch": [0.05, 0.05, 0.1, 0.1, -0.05],        # 抚摸交互行为
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
            Momentum decay factor controlling update smoothness. 默认为 ``0.9``。
            Personality updates apply ``new = momentum * old + (1 - momentum) * delta``
            so 0.9 keeps 90% of the previous value and 10% of the new delta.
        behavior_map: dict | None, optional
            Mapping from behavior tag to OCEAN vector deltas. 如未提供，
            默认使用 :data:`DEFAULT_BEHAVIOR_MAP`。
        """
        # OCEAN: Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism
        # OCEAN：开放性、责任心、外向性、宜人性、神经质
        if not 0.0 <= momentum <= 1.0:
            raise ValueError("momentum must be between 0 and 1")
        self.vector = list(DEFAULT_PERSONALITY_VECTOR)  # 初始外向人格
        self.momentum = momentum  # 动量衰减因子
        # 行为标签映射表，可自定义传入
        self.behavior_map = behavior_map or DEFAULT_BEHAVIOR_MAP
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(LOG_LEVEL)

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
        if len(delta) != 5:
            raise ValueError("behavior delta must have 5 dimensions")
        self.logger.debug("Updating personality with tag %s", behavior_tag)
        # 使用动量衰减更新人格向量，确保变化平滑并限制范围在 [-1, 1]
        self.vector = [
            max(-1.0, min(1.0, self.momentum * v + (1 - self.momentum) * d))
            for v, d in zip(self.vector, delta)
        ]
        self.logger.debug("New personality vector: %s", self.vector)

    def get_personality_style(self) -> str:
        """Return a simple language tone based on current personality.

        根据当前的人格向量返回语言风格。
        """
        extroversion = self.vector[2]  # index 2 corresponds to Extraversion
        if extroversion > 0.5:
            # 高外向性 -> 热情
            style = "enthusiastic"
        elif extroversion < -0.5:
            # 低外向性 -> 冷淡
            style = "cold"
        else:
            style = "neutral"
        self.logger.debug("Personality style: %s", style)
        return style

    def get_dominant_traits(self) -> list[str]:
        """Get dominant personality traits based on OCEAN vector.

        根据OCEAN向量获取主导人格特质。
        """
        traits = []
        trait_names = ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]
        
        for i, value in enumerate(self.vector):
            if value > 0.3:
                traits.append(f"high_{trait_names[i]}")
            elif value < -0.3:
                traits.append(f"low_{trait_names[i]}")
        
        self.logger.debug("Dominant traits: %s", traits)
        return traits

    def get_personality_summary(self) -> str:
        """Get a comprehensive personality summary.

        获取综合人格描述。
        """
        traits = self.get_dominant_traits()
        style = self.get_personality_style()
        
        summary_parts = []
        if traits:
            summary_parts.append(f"Traits: {', '.join(traits)}")
        if style != "neutral":
            summary_parts.append(f"Style: {style}")
        
        summary = " | ".join(summary_parts) if summary_parts else "neutral"
        self.logger.debug("Personality summary: %s", summary)
        return summary

    def get_vector(self):
        """Return a copy of the current OCEAN vector.

        返回当前人格向量的副本，避免外部修改。
        """
        return list(self.vector)