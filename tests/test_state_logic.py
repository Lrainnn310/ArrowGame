"""单关卡状态和 Restart 逻辑的单元测试。"""

import unittest

from models import Arrow, Direction, GameState
from state_logic import (
    clone_board,
    has_arrows,
    restart_game,
    state_after_blocked_click,
    state_after_successful_removal,
)


class TestStateLogic(unittest.TestCase):
    def test_clearing_last_arrow_passes_level(self):
        arrow = Arrow(0, 0, Direction.RIGHT)
        board = [[arrow]]
        board[0][0] = None

        self.assertFalse(has_arrows(board))
        self.assertEqual(state_after_successful_removal(board), GameState.PASSED)

    def test_zero_mistakes_causes_failure(self):
        self.assertEqual(state_after_blocked_click(0), GameState.FAILED)

    def test_positive_mistakes_keeps_playing(self):
        self.assertEqual(state_after_blocked_click(1), GameState.PLAYING)

    def test_restart_restores_mistakes_value(self):
        initial_board = [[Arrow(0, 0, Direction.RIGHT)]]
        _, remaining_mistakes, game_state = restart_game(initial_board)

        self.assertEqual(remaining_mistakes, 3)
        self.assertEqual(game_state, GameState.PLAYING)

    def test_restart_restores_deleted_arrow(self):
        initial_board = [[Arrow(0, 0, Direction.RIGHT), None]]
        board = clone_board(initial_board)
        board[0][0] = None
        board, _, _ = restart_game(initial_board)

        self.assertIsNotNone(board[0][0])
        self.assertEqual(board[0][0], initial_board[0][0])

    def test_game_board_copy_does_not_modify_initial_layout(self):
        initial_board = [[Arrow(0, 0, Direction.RIGHT), None]]
        game_board = clone_board(initial_board)
        game_board[0][0] = None

        self.assertIsNotNone(initial_board[0][0])
        self.assertIsNone(game_board[0][0])
        self.assertIsNot(game_board, initial_board)
        self.assertIsNot(game_board[0], initial_board[0])


if __name__ == "__main__":
    unittest.main()
