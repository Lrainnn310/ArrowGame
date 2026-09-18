"""Stage 4 的基础点击处理逻辑。"""

from path_detection import is_blocked


def find_arrow(board, row, col):
    """返回指定棋盘位置的箭头；空格或越界时返回 None。"""
    if not board or not board[0]:
        return None
    if not (0 <= row < len(board) and 0 <= col < len(board[0])):
        return None
    return board[row][col]


def process_arrow_click(board, row, col, remaining_mistakes):
    """处理一次棋盘点击，返回更新后的错误次数和是否碰撞。

    成功时将箭头所在位置设置为 None；被阻挡时保留箭头并扣除一次错误次数。
    """
    arrow = find_arrow(board, row, col)
    if arrow is None:
        return remaining_mistakes, False

    if is_blocked(board, arrow):
        return max(0, remaining_mistakes - 1), True

    board[row][col] = None
    return remaining_mistakes, False
