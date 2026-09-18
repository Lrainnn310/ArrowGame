"""正式关卡和关卡切换测试。"""

import unittest

from board import LEVELS
from game_logic import process_arrow_click
from models import GameState
from state_logic import (
    advance_level,
    has_arrows,
    restart_current_level,
    restart_whole_game,
    state_after_successful_removal,
    navigate_level,
)


# 每个坐标序列都是经过路径检测的合法清除顺序。
SOLUTIONS = [
    [(0, 0), (0, 5), (5, 0), (5, 5)],
    [(1, 4), (1, 2), (1, 0), (3, 1), (3, 3), (3, 5)],
    [(0, 0), (1, 4), (1, 2), (1, 0), (3, 1), (3, 3), (3, 5), (5, 5)],
]


def clear_level(level_index):
    board = [row[:] for row in LEVELS[level_index]]
    mistakes = 3
    for row, col in SOLUTIONS[level_index]:
        mistakes, collided = process_arrow_click(board, row, col, mistakes)
        if collided:
            raise AssertionError(f"预定义顺序在 {row}, {col} 处被阻挡")
    return board, mistakes


class TestLevels(unittest.TestCase):
    def test_level_navigation_boundaries(self):
        self.assertIsNone(navigate_level(LEVELS, 0, -1))
        self.assertIsNone(navigate_level(LEVELS, 2, 1))

    def test_level_navigation_loads_fresh_target_level(self):
        result = navigate_level(LEVELS, 1, -1)
        index, board, mistakes, state = result
        board[0][0] = None
        self.assertEqual(index, 0)
        self.assertEqual(mistakes, 3)
        self.assertEqual(state, GameState.PLAYING)
        self.assertEqual(board[1], LEVELS[0][1])
        self.assertNotEqual(board, LEVELS[0])

    def test_there_are_three_levels(self):
        self.assertEqual(len(LEVELS), 3)

    def test_all_levels_have_a_valid_solution(self):
        for level_index in range(3):
            with self.subTest(level=level_index + 1):
                board, mistakes = clear_level(level_index)
                self.assertFalse(has_arrows(board))
                self.assertEqual(mistakes, 3)
                self.assertEqual(state_after_successful_removal(board), GameState.PASSED)

    def test_level_one_can_advance_to_level_two(self):
        current_index, _, _, _ = restart_whole_game(LEVELS)
        current_index, board, mistakes, state = advance_level(LEVELS, current_index)
        self.assertEqual(current_index, 1)
        self.assertEqual(len(board), 6)
        self.assertEqual(mistakes, 3)
        self.assertEqual(state, GameState.PLAYING)

    def test_level_two_can_advance_to_level_three(self):
        current_index, board, _, _ = restart_whole_game(LEVELS)
        current_index, board, _, _ = advance_level(LEVELS, current_index)
        current_index, board, mistakes, state = advance_level(LEVELS, current_index)
        self.assertEqual(current_index, 2)
        self.assertTrue(has_arrows(board))
        self.assertEqual(mistakes, 3)
        self.assertEqual(state, GameState.PLAYING)

    def test_restart_current_level_keeps_level_two(self):
        current_index, _, _, _ = restart_whole_game(LEVELS)
        current_index, board, _, _ = advance_level(LEVELS, current_index)
        board[1][4] = None
        restarted_index, restarted_board, mistakes, state = restart_current_level(
            LEVELS, current_index
        )
        self.assertEqual(restarted_index, 1)
        self.assertIsNotNone(restarted_board[1][4])
        self.assertEqual(mistakes, 3)
        self.assertEqual(state, GameState.PLAYING)

    def test_last_level_is_all_clear(self):
        board, _ = clear_level(2)
        self.assertEqual(state_after_successful_removal(board), GameState.PASSED)
        self.assertEqual(2, len(LEVELS) - 1)

    def test_restart_whole_game_returns_to_level_one(self):
        current_index, board, mistakes, state = restart_whole_game(LEVELS)
        self.assertEqual(current_index, 0)
        self.assertEqual(board, LEVELS[0])
        self.assertEqual(mistakes, 3)
        self.assertEqual(state, GameState.PLAYING)
        self.assertIsNot(board, LEVELS[0])
        self.assertIsNot(board[0], LEVELS[0][0])


if __name__ == "__main__":
    unittest.main()
