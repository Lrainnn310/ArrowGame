"""游戏中使用的基础数据结构。"""

from dataclasses import dataclass
from enum import Enum


class Direction(Enum):
    """箭头的四种方向。"""

    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class GameState(Enum):
    """当前单关卡的游戏状态。"""

    PLAYING = "playing"
    PASSED = "passed"
    FAILED = "failed"


@dataclass(frozen=True)
class Arrow:
    """表示棋盘中的一个箭头。"""

    row: int
    col: int
    direction: Direction
