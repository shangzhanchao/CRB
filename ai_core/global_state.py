"""Global metrics for the Companion Robot Intelligent Brain.

陪伴机器人智能大脑在运行时收集的全局数据，包括交互次数、
系统启动时间与已收集的语音时长等。这些统计量用于判定成长
阶段，影响对话复杂度与回应方式。
"""

from __future__ import annotations

import datetime

# use timezone-aware UTC timestamps
import wave

INTERACTION_COUNT = 0  # 总交互次数
START_TIME = datetime.datetime.now(datetime.timezone.utc)  # 系统启动时间
AUDIO_DATA_SECONDS = 0.0  # 累计语音时长（秒）


def increment() -> int:
    """Increase global interaction count and return new value.

    递增全局交互计数器并返回最新值。
    """

    global INTERACTION_COUNT
    INTERACTION_COUNT += 1
    return INTERACTION_COUNT


def add_audio_duration(path: str) -> float:
    """Add duration of given audio file to total seconds.

    累加语音文件的时长。若无法读取，则记为 0。
    """

    global AUDIO_DATA_SECONDS
    try:
        with wave.open(path, "rb") as wf:
            AUDIO_DATA_SECONDS += wf.getnframes() / float(wf.getframerate())
    except Exception:  # pragma: no cover - unreadable file
        pass
    return AUDIO_DATA_SECONDS


def days_since_start() -> int:
    """Return integer days since system start.

    计算自系统启动以来经过的整天数。
    """

    delta = datetime.datetime.now(datetime.timezone.utc) - START_TIME
    return delta.days


def get_growth_stage() -> str:
    """Compute growth stage from runtime statistics.

    根据时间、交互次数与语音数据量，推断机器人所处的语言成长
    阶段，阶段值用于控制对话引擎的表现。"""

    days = days_since_start()
    if days < 3 or INTERACTION_COUNT < 5 or AUDIO_DATA_SECONDS < 60:
        return "sprout"  # 萌芽期
    if days < 10 or INTERACTION_COUNT < 20 or AUDIO_DATA_SECONDS < 300:
        return "enlighten"  # 启蒙期
    if days < 30 or INTERACTION_COUNT < 50 or AUDIO_DATA_SECONDS < 900:
        return "resonate"  # 共鸣期
    return "awaken"  # 觉醒期


def reset() -> None:
    """Reset global counters and timers.

    重置全局交互次数、累计语音时长和启动时间，以便测试或重启
    系统时回到初始状态。"""

    global INTERACTION_COUNT, AUDIO_DATA_SECONDS, START_TIME
    INTERACTION_COUNT = 0
    AUDIO_DATA_SECONDS = 0.0
    START_TIME = datetime.datetime.now(datetime.timezone.utc)
