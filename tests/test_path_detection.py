"""路径检测算法的单元测试。"""

import unittest

from models import Arrow, Direction
from path_detection import is_blocked


def empty_board(size=5):
    return [[None for _ in range(size)] for _ in range(size)]


class TestIsBlocked(unittest.TestCase):
    def test_up_without_obstacle(self):
        board = empty_board()
        arrow = Arrow(3, 2, Direction.UP)
        board[3][2] = arrow
        self.assertFalse(is_blocked(board, arrow))

    def test_up_with_obstacle(self):
        board = empty_board()
        arrow = Arrow(3, 2, Direction.UP)
        board[3][2] = arrow
        board[1][2] = Arrow(1, 2, Direction.DOWN)
        self.assertTrue(is_blocked(board, arrow))

    def test_down_without_obstacle(self):
        board = empty_board()
        arrow = Arrow(1, 2, Direction.DOWN)
        board[1][2] = arrow
        self.assertFalse(is_blocked(board, arrow))

    def test_down_with_obstacle(self):
        board = empty_board()
        arrow = Arrow(1, 2, Direction.DOWN)
        board[1][2] = arrow
        board[4][2] = Arrow(4, 2, Direction.UP)
        self.assertTrue(is_blocked(board, arrow))

    def test_left_without_obstacle(self):
        board = empty_board()
        arrow = Arrow(2, 3, Direction.LEFT)
        board[2][3] = arrow
        self.assertFalse(is_blocked(board, arrow))

    def test_left_with_obstacle(self):
        board = empty_board()
        arrow = Arrow(2, 3, Direction.LEFT)
        board[2][3] = arrow
        board[2][0] = Arrow(2, 0, Direction.RIGHT)
        self.assertTrue(is_blocked(board, arrow))

    def test_right_without_obstacle(self):
        board = empty_board()
        arrow = Arrow(2, 1, Direction.RIGHT)
        board[2][1] = arrow
        self.assertFalse(is_blocked(board, arrow))

    def test_right_with_obstacle(self):
        board = empty_board()
        arrow = Arrow(2, 1, Direction.RIGHT)
        board[2][1] = arrow
        board[2][4] = Arrow(2, 4, Direction.LEFT)
        self.assertTrue(is_blocked(board, arrow))

    def test_multiple_empty_cells_before_obstacle(self):
        board = empty_board()
        arrow = Arrow(4, 0, Direction.UP)
        board[4][0] = arrow
        board[1][0] = Arrow(1, 0, Direction.DOWN)
        self.assertTrue(is_blocked(board, arrow))

    def test_edge_arrow_facing_outward_is_not_blocked(self):
        cases = [
            (Arrow(0, 2, Direction.UP)),
            (Arrow(4, 2, Direction.DOWN)),
            (Arrow(2, 0, Direction.LEFT)),
            (Arrow(2, 4, Direction.RIGHT)),
        ]

        for arrow in cases:
            board = empty_board()
            board[arrow.row][arrow.col] = arrow
            with self.subTest(direction=arrow.direction):
                self.assertFalse(is_blocked(board, arrow))

    def test_current_arrow_is_not_an_obstacle(self):
        board = empty_board()
        arrow = Arrow(2, 2, Direction.RIGHT)
        board[2][2] = arrow
        self.assertFalse(is_blocked(board, arrow))


if __name__ == "__main__":
    unittest.main()
