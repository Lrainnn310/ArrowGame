"""基础点击处理逻辑的单元测试。"""

import unittest

from game_logic import process_arrow_click
from models import Arrow, Direction


class TestGameLogic(unittest.TestCase):
    def test_unblocked_arrow_is_removed(self):
        arrow = Arrow(1, 1, Direction.UP)
        board = [[None for _ in range(3)] for _ in range(3)]
        board[1][1] = arrow

        mistakes, collided = process_arrow_click(board, 1, 1, 3)

        self.assertIsNone(board[1][1])
        self.assertEqual(mistakes, 3)
        self.assertFalse(collided)

    def test_blocked_arrow_remains_and_mistake_decreases(self):
        arrow = Arrow(2, 1, Direction.UP)
        board = [[None for _ in range(3)] for _ in range(3)]
        board[2][1] = arrow
        board[0][1] = Arrow(0, 1, Direction.DOWN)

        mistakes, collided = process_arrow_click(board, 2, 1, 3)

        self.assertIs(board[2][1], arrow)
        self.assertEqual(mistakes, 2)
        self.assertTrue(collided)

    def test_empty_or_outside_click_does_not_change_mistakes(self):
        board = [[None for _ in range(3)] for _ in range(3)]

        mistakes, collided = process_arrow_click(board, 1, 1, 3)
        self.assertEqual((mistakes, collided), (3, False))

        mistakes, collided = process_arrow_click(board, -1, 1, mistakes)
        self.assertEqual((mistakes, collided), (3, False))


if __name__ == "__main__":
    unittest.main()
