"""单关卡游戏状态和棋盘重置逻辑。"""

from models import GameState


INITIAL_MISTAKES = 3


def clone_board(board):
    """创建独立的棋盘副本。

    Arrow 是不可变数据对象，因此复制二维列表即可避免棋盘结构共享。
    """
    return [row[:] for row in board]


def restart_game(initial_board):
    """返回重新开始所需的独立棋盘、错误次数和游戏状态。"""
    return clone_board(initial_board), INITIAL_MISTAKES, GameState.PLAYING


def has_arrows(board):
    """判断棋盘上是否还存在箭头。"""
    return any(arrow is not None for row in board for arrow in row)


def state_after_successful_removal(board):
    """成功移除箭头后，根据棋盘是否清空返回游戏状态。"""
    if has_arrows(board):
        return GameState.PLAYING
    return GameState.PASSED


def state_after_blocked_click(remaining_mistakes):
    """根据剩余错误次数判断阻挡点击后的游戏状态。"""
    if remaining_mistakes <= 0:
        return GameState.FAILED
    return GameState.PLAYING
