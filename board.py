"""棋盘和箭头的绘制逻辑。"""

import pygame

from models import Arrow, Direction


BOARD_ROWS = 6
BOARD_COLS = 6
CELL_SIZE = 70
BOARD_X = 190
BOARD_Y = 70
GRID_COLOR = (190, 190, 190)
ARROW_COLOR = (80, 190, 255)
COLLISION_COLOR = (255, 90, 90)


# Level 1: 四个朝棋盘外的箭头，适合熟悉基本操作。
LEVEL_1 = [
    [Arrow(0, 0, Direction.UP), None, None, None, None, Arrow(0, 5, Direction.RIGHT)],
    [None, None, None, None, None, None],
    [None, None, None, None, None, None],
    [None, None, None, None, None, None],
    [None, None, None, None, None, None],
    [Arrow(5, 0, Direction.LEFT), None, None, None, None, Arrow(5, 5, Direction.DOWN)],
]

# Level 2: 两条横向阻挡链，必须先清除链条末端。
LEVEL_2 = [
    [None, None, None, None, None, None],
    [Arrow(1, 0, Direction.RIGHT), None, Arrow(1, 2, Direction.RIGHT), None, Arrow(1, 4, Direction.RIGHT), None],
    [None, None, None, None, None, None],
    [None, Arrow(3, 1, Direction.LEFT), None, Arrow(3, 3, Direction.LEFT), None, Arrow(3, 5, Direction.LEFT)],
    [None, None, None, None, None, None],
    [None, None, None, None, None, None],
]

# Level 3: 三条独立方向链，箭头数量更多但仍有明确的合法顺序。
LEVEL_3 = [
    [Arrow(0, 0, Direction.UP), None, None, None, None, None],
    [Arrow(1, 0, Direction.RIGHT), None, Arrow(1, 2, Direction.RIGHT), None, Arrow(1, 4, Direction.RIGHT), None],
    [None, None, None, None, None, None],
    [None, Arrow(3, 1, Direction.LEFT), None, Arrow(3, 3, Direction.LEFT), None, Arrow(3, 5, Direction.LEFT)],
    [None, None, None, None, None, None],
    [None, None, None, None, None, Arrow(5, 5, Direction.DOWN)],
]


LEVELS = [LEVEL_1, LEVEL_2, LEVEL_3]

# 保留旧名称，兼容此前代码和文档。
TEST_BOARD = LEVEL_1


OLD_TEST_BOARD = [
    [Arrow(0, 0, Direction.RIGHT), None, None, None, None, Arrow(0, 5, Direction.DOWN)],
    [None, None, None, None, None, None],
    [None, None, Arrow(2, 2, Direction.UP), None, None, None],
    [None, None, None, None, None, None],
    [None, None, None, None, Arrow(4, 4, Direction.LEFT), None],
    [None, None, None, None, None, None],
]


def draw_board(screen, board, collision_cell=None):
    """绘制网格及指定位置的箭头。"""
    board_rect = pygame.Rect(
        BOARD_X,
        BOARD_Y,
        BOARD_COLS * CELL_SIZE,
        BOARD_ROWS * CELL_SIZE,
    )
    pygame.draw.rect(screen, (45, 45, 45), board_rect)

    for row in range(BOARD_ROWS + 1):
        y = BOARD_Y + row * CELL_SIZE
        pygame.draw.line(screen, GRID_COLOR, (BOARD_X, y), (board_rect.right, y), 2)

    for col in range(BOARD_COLS + 1):
        x = BOARD_X + col * CELL_SIZE
        pygame.draw.line(screen, GRID_COLOR, (x, BOARD_Y), (x, board_rect.bottom), 2)

    for row in board:
        for arrow in row:
            if arrow is not None:
                is_collision = collision_cell == (arrow.row, arrow.col)
                draw_arrow(screen, arrow, is_collision)


def draw_arrow(screen, arrow, is_collision=False):
    """将箭头绘制在所在格子的中央。"""
    center_x = BOARD_X + arrow.col * CELL_SIZE + CELL_SIZE // 2
    center_y = BOARD_Y + arrow.row * CELL_SIZE + CELL_SIZE // 2
    half_length = 22
    head_length = 14
    head_width = 13

    if arrow.direction == Direction.UP:
        points = [
            (center_x, center_y - half_length),
            (center_x - head_width, center_y - half_length + head_length),
            (center_x - 4, center_y - half_length + head_length),
            (center_x - 4, center_y + half_length),
            (center_x + 4, center_y + half_length),
            (center_x + 4, center_y - half_length + head_length),
            (center_x + head_width, center_y - half_length + head_length),
        ]
    elif arrow.direction == Direction.DOWN:
        points = [
            (center_x, center_y + half_length),
            (center_x - head_width, center_y + half_length - head_length),
            (center_x - 4, center_y + half_length - head_length),
            (center_x - 4, center_y - half_length),
            (center_x + 4, center_y - half_length),
            (center_x + 4, center_y + half_length - head_length),
            (center_x + head_width, center_y + half_length - head_length),
        ]
    elif arrow.direction == Direction.LEFT:
        points = [
            (center_x - half_length, center_y),
            (center_x - half_length + head_length, center_y - head_width),
            (center_x - half_length + head_length, center_y - 4),
            (center_x + half_length, center_y - 4),
            (center_x + half_length, center_y + 4),
            (center_x - half_length + head_length, center_y + 4),
            (center_x - half_length + head_length, center_y + head_width),
        ]
    else:
        points = [
            (center_x + half_length, center_y),
            (center_x + half_length - head_length, center_y - head_width),
            (center_x + half_length - head_length, center_y - 4),
            (center_x - half_length, center_y - 4),
            (center_x - half_length, center_y + 4),
            (center_x + half_length - head_length, center_y + 4),
            (center_x + half_length - head_length, center_y + head_width),
        ]

    color = COLLISION_COLOR if is_collision else ARROW_COLOR
    pygame.draw.polygon(screen, color, points)
