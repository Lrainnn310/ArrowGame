"""箭头路径检测算法。"""

from models import Arrow, Direction


DIRECTION_VECTORS = {
    Direction.UP: (-1, 0),
    Direction.DOWN: (1, 0),
    Direction.LEFT: (0, -1),
    Direction.RIGHT: (0, 1),
}


def is_blocked(board, arrow):
    """判断箭头沿自身方向到棋盘边界之间是否存在其他箭头。

    board 是二维列表，空位置使用 None，箭头位置使用 Arrow 对象。
    """
    row_step, col_step = DIRECTION_VECTORS[arrow.direction]
    row = arrow.row + row_step
    col = arrow.col + col_step

    while 0 <= row < len(board) and 0 <= col < len(board[0]):
        if board[row][col] is not None:
            return True
        row += row_step
        col += col_step

    return False
