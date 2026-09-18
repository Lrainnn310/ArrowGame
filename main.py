"""Arrow Game 的程序入口。"""

import pygame

from board import BOARD_X, BOARD_Y, BOARD_COLS, BOARD_ROWS, CELL_SIZE, LEVELS, draw_board
from game_logic import process_arrow_click
from models import GameState
from state_logic import (
    advance_level,
    restart_current_level,
    restart_whole_game,
    state_after_blocked_click,
    state_after_successful_removal,
)


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Arrow Game"
BACKGROUND_COLOR = (30, 30, 30)
TEXT_COLOR = (240, 240, 240)
BUTTON_COLOR = (70, 110, 170)
BUTTON_HOVER_COLOR = (90, 140, 210)
COLLISION_FEEDBACK_SECONDS = 0.35
RESTART_BUTTON_RECT = pygame.Rect(470, 20, 130, 36)


def mouse_to_cell(position):
    """将窗口坐标转换为棋盘行列；棋盘外返回 None。"""
    mouse_x, mouse_y = position
    col = (mouse_x - BOARD_X) // CELL_SIZE
    row = (mouse_y - BOARD_Y) // CELL_SIZE
    if 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLS:
        return row, col
    return None


def main():
    """初始化 Pygame 并运行基础游戏循环。"""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)

    running = True
    clock = pygame.time.Clock()
    current_level_index, board, remaining_mistakes, game_state = restart_whole_game(LEVELS)
    collision_cell = None
    collision_until = 0
    font = pygame.font.Font(None, 32)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if RESTART_BUTTON_RECT.collidepoint(event.pos):
                    if game_state == GameState.PASSED and current_level_index == len(LEVELS) - 1:
                        current_level_index, board, remaining_mistakes, game_state = restart_whole_game(LEVELS)
                    elif game_state == GameState.PASSED:
                        current_level_index, board, remaining_mistakes, game_state = advance_level(
                            LEVELS, current_level_index
                        )
                    else:
                        current_level_index, board, remaining_mistakes, game_state = restart_current_level(
                            LEVELS, current_level_index
                        )
                    collision_cell = None
                    collision_until = 0
                elif game_state == GameState.PLAYING:
                    cell = mouse_to_cell(event.pos)
                    if cell is not None:
                        row, col = cell
                        previous_mistakes = remaining_mistakes
                        previous_arrow = board[row][col]
                        remaining_mistakes, collided = process_arrow_click(
                            board, row, col, remaining_mistakes
                        )
                        if collided:
                            if remaining_mistakes < previous_mistakes:
                                collision_cell = cell
                                collision_until = pygame.time.get_ticks() + int(
                                    COLLISION_FEEDBACK_SECONDS * 1000
                                )
                            game_state = state_after_blocked_click(remaining_mistakes)
                        elif previous_arrow is not None:
                            game_state = state_after_successful_removal(board)

        screen.fill(BACKGROUND_COLOR)
        if collision_cell is not None and pygame.time.get_ticks() >= collision_until:
            collision_cell = None
        draw_board(screen, board, collision_cell)
        level_text = f"Level: {current_level_index + 1} / {len(LEVELS)}"
        level_surface = font.render(level_text, True, TEXT_COLOR)
        screen.blit(level_surface, (190, 5))

        if game_state == GameState.PLAYING:
            status_text = f"Remaining Mistakes: {remaining_mistakes}"
        elif game_state == GameState.PASSED:
            status_text = "All Levels Clear!" if current_level_index == len(LEVELS) - 1 else "Level Clear!"
        else:
            status_text = "Game Over"
        status = font.render(status_text, True, TEXT_COLOR)
        screen.blit(status, (190, 35))

        button_color = (
            BUTTON_HOVER_COLOR
            if RESTART_BUTTON_RECT.collidepoint(pygame.mouse.get_pos())
            else BUTTON_COLOR
        )
        pygame.draw.rect(screen, button_color, RESTART_BUTTON_RECT, border_radius=5)
        if game_state == GameState.PASSED and current_level_index < len(LEVELS) - 1:
            button_text = "Next Level"
        elif game_state == GameState.PASSED:
            button_text = "Restart Game"
        else:
            button_text = "Restart"
        restart_text = font.render(button_text, True, TEXT_COLOR)
        restart_position = restart_text.get_rect(center=RESTART_BUTTON_RECT.center)
        screen.blit(restart_text, restart_position)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
