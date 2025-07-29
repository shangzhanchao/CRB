"""Global state for AI companion.

交互计数器等全局变量存放在此模块。
"""

INTERACTION_COUNT = 0


def increment() -> int:
    """Increase global interaction count and return new value.

    递增全局交互计数器并返回最新值。
    """
    global INTERACTION_COUNT
    INTERACTION_COUNT += 1
    return INTERACTION_COUNT


def reset() -> None:
    """Reset global interaction counter.

    重置全局交互计数器。
    """
    global INTERACTION_COUNT
    INTERACTION_COUNT = 0
