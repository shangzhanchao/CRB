"""Global metrics for the Companion Robot Intelligent Brain.

陪伴机器人智能大脑在运行时收集的全局数据，包括交互次数、
系统启动时间与已收集的语音时长等。这些统计量用于判定成长
阶段，影响对话复杂度与回应方式。
"""

from __future__ import annotations

import datetime
import logging

# use timezone-aware UTC timestamps
import wave

from .constants import (
    DEFAULT_GROWTH_STAGE,
    INITIAL_INTERACTIONS,
    INITIAL_AUDIO_SECONDS,
    STAGE_THRESHOLDS,  # 成长阶段阈值参数
    STAGE_ORDER,       # 成长阶段顺序
    LOG_LEVEL,
    ROBOT_ID_WHITELIST,  # 允许的机器人编号
    STATE_FILE,         # 全局状态文件路径
)

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)

import atexit



def is_robot_allowed(robot_id: str) -> bool:
    """Check if the robot ID is in the whitelist.

    判断机器人编号是否在白名单 ``ROBOT_ID_WHITELIST`` 中。
    """
    allowed = robot_id in ROBOT_ID_WHITELIST
    if not allowed:
        logger.warning("Robot %s not in whitelist", robot_id)
    return allowed

INTERACTION_COUNT = INITIAL_INTERACTIONS  # 总交互次数
START_TIME = datetime.datetime.now(datetime.timezone.utc)  # 系统启动时间
AUDIO_DATA_SECONDS = INITIAL_AUDIO_SECONDS  # 累计语音时长（秒）


def increment() -> int:
    """Increase global interaction count and return new value.

    递增全局交互计数器并返回最新值。
    """

    global INTERACTION_COUNT
    INTERACTION_COUNT += 1
    logger.debug("Interaction count incremented to %s", INTERACTION_COUNT)
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
    logger.debug("Total audio seconds: %s", AUDIO_DATA_SECONDS)
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
    if INTERACTION_COUNT == INITIAL_INTERACTIONS and AUDIO_DATA_SECONDS == INITIAL_AUDIO_SECONDS:
        logger.debug("Using default growth stage: %s", DEFAULT_GROWTH_STAGE)
        return DEFAULT_GROWTH_STAGE

    for stage in STAGE_ORDER[:-1]:
        thr = STAGE_THRESHOLDS.get(stage)
        if not thr:
            continue
        if (
            days < thr["days"]
            or INTERACTION_COUNT < thr["interactions"]
            or AUDIO_DATA_SECONDS < thr["audio_seconds"]
        ):
            logger.debug("Growth stage %s", stage)
            return stage

    final_stage = STAGE_ORDER[-1]
    logger.debug("Growth stage %s", final_stage)
    return final_stage  # 觉醒期


def reset() -> None:
    """Reset global counters and timers.

    重置全局交互次数、累计语音时长和启动时间，以便测试或重启
    系统时回到初始状态。"""

    global INTERACTION_COUNT, AUDIO_DATA_SECONDS, START_TIME
    INTERACTION_COUNT = INITIAL_INTERACTIONS
    AUDIO_DATA_SECONDS = INITIAL_AUDIO_SECONDS
    START_TIME = datetime.datetime.now(datetime.timezone.utc)
    logger.debug("Global state reset")


def save_state(path: str) -> None:
    """Persist global counters to a JSON file.

    将当前全局统计数据保存到 JSON 文件。
    """

    import json

    data = {
        "interaction_count": INTERACTION_COUNT,
        "audio_seconds": AUDIO_DATA_SECONDS,
        "start_time": START_TIME.isoformat(),
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh)
    logger.info("Global state saved to %s", path)


def load_state(path: str) -> None:
    """Load global counters from a JSON file if present.

    从 JSON 文件中恢复全局统计数据（若文件存在）。
    """

    import json
    import os

    if not os.path.exists(path):
        logger.warning("State file %s not found", path)
        return
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    global INTERACTION_COUNT, AUDIO_DATA_SECONDS, START_TIME
    INTERACTION_COUNT = int(data.get("interaction_count", INITIAL_INTERACTIONS))
    AUDIO_DATA_SECONDS = float(data.get("audio_seconds", INITIAL_AUDIO_SECONDS))
    try:
        START_TIME = datetime.datetime.fromisoformat(data.get("start_time"))
    except Exception:
        START_TIME = datetime.datetime.now(datetime.timezone.utc)
    logger.info("Global state loaded from %s", path)


def get_growth_metrics() -> dict:
    """Return current metrics for visualization.

    返回当前的成长指标，用于可视化展示。"""

    return {
        "interaction_count": INTERACTION_COUNT,
        "audio_seconds": AUDIO_DATA_SECONDS,
        "days": days_since_start(),
        "stage": get_growth_stage(),
    }


# 初始化加载和注册退出保存
load_state(STATE_FILE)
atexit.register(save_state, STATE_FILE)