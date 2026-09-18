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


def restart_current_level(levels, current_level_index):
    """重新开始当前关卡，不改变关卡编号。"""
    board = clone_board(levels[current_level_index])
    return current_level_index, board, INITIAL_MISTAKES, GameState.PLAYING


def advance_level(levels, current_level_index):
    """进入下一关，并返回新的关卡状态。"""
    next_index = current_level_index + 1
    if next_index >= len(levels):
        raise ValueError("已经是最后一个关卡，不能继续进入下一关")
    board = clone_board(levels[next_index])
    return next_index, board, INITIAL_MISTAKES, GameState.PLAYING


def navigate_level(levels, current_level_index, offset):
    """按 offset 浏览关卡，并安全处理第一关和最后一关边界。"""
    target_index = current_level_index + offset
    if not 0 <= target_index < len(levels):
        return None
    return target_index, clone_board(levels[target_index]), INITIAL_MISTAKES, GameState.PLAYING


def restart_whole_game(levels):
    """从第一关重新开始整个游戏。"""
    return 0, clone_board(levels[0]), INITIAL_MISTAKES, GameState.PLAYING


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
