"""Arrow Game 的程序入口和基础界面。"""

import pygame

from board import (
    BOARD_COLS,
    BOARD_ROWS,
    BOARD_X,
    BOARD_Y,
    CELL_SIZE,
    LEVELS,
    draw_board,
    draw_flying_arrow,
)
from game_logic import process_arrow_click
from models import FlyingArrow, GameState
from state_logic import (
    advance_level,
    navigate_level,
    restart_current_level,
    restart_whole_game,
    state_after_blocked_click,
    state_after_successful_removal,
)


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 700
WINDOW_TITLE = "一箭又一箭"
BACKGROUND_COLOR = (255, 246, 232)
TEXT_COLOR = (72, 45, 95)
SUBTLE_TEXT_COLOR = (105, 75, 125)
BUTTON_COLOR = (255, 132, 177)
BUTTON_HOVER_COLOR = (255, 104, 155)
DISABLED_BUTTON_COLOR = (215, 205, 220)
START_BUTTON_RECT = pygame.Rect(265, 430, 270, 52)
PREVIOUS_BUTTON_RECT = pygame.Rect(175, 125, 135, 42)
NEXT_BUTTON_RECT = pygame.Rect(330, 125, 135, 42)
ACTION_BUTTON_RECT = pygame.Rect(485, 125, 180, 42)
COLLISION_FEEDBACK_SECONDS = 0.35
FLYING_DURATION_MS = 300


def mouse_to_cell(position):
    """将窗口坐标转换为棋盘行列；棋盘外返回 None。"""
    mouse_x, mouse_y = position
    col = (mouse_x - BOARD_X) // CELL_SIZE
    row = (mouse_y - BOARD_Y) // CELL_SIZE
    if 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLS:
        return row, col
    return None


def load_font(size):
    """优先使用 Windows 常见中文字体，并提供系统字体回退。"""
    for name in ("microsoftyahei", "simhei", "simsun", "arialunicode" ):
        font = pygame.font.SysFont(name, size)
        if font is not None:
            return font
    return pygame.font.Font(None, size)


def draw_button(screen, rect, label, font, enabled=True):
    """绘制圆角按钮，文字按实际尺寸居中。"""
    if not enabled:
        color = DISABLED_BUTTON_COLOR
    else:
        color = BUTTON_HOVER_COLOR if rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
    shadow = rect.move(0, 4)
    pygame.draw.rect(screen, (220, 175, 195), shadow, border_radius=12)
    pygame.draw.rect(screen, color, rect, border_radius=12)
    text = font.render(label, True, TEXT_COLOR if enabled else (150, 140, 155))
    screen.blit(text, text.get_rect(center=rect.center))


def draw_start_screen(screen, title_font, font):
    """绘制开始界面。"""
    title = title_font.render("一箭又一箭", True, TEXT_COLOR)
    screen.blit(title, title.get_rect(center=(WINDOW_WIDTH // 2, 135)))
    decorations = [("↑", (255, 105, 180)), ("→", (255, 165, 70)),
                   ("↓", (70, 175, 245)), ("←", (165, 105, 235))]
    for index, (symbol, color) in enumerate(decorations):
        text = title_font.render(symbol, True, color)
        screen.blit(text, text.get_rect(center=(285 + index * 78, 195)))
    lines = [
        "点击前方没有阻挡的箭头，",
        "让所有箭头飞出棋盘！",
        "小心被阻挡的箭头，",
        "你有 3 次失误机会。",
    ]
    for index, line in enumerate(lines):
        text = font.render(line, True, SUBTLE_TEXT_COLOR)
        screen.blit(text, text.get_rect(center=(WINDOW_WIDTH // 2, 255 + index * 30)))
    draw_button(screen, START_BUTTON_RECT, "开始游戏", font)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()
    title_font = load_font(52)
    font = load_font(28)
    small_font = load_font(24)

    current_level_index, board, remaining_mistakes, _ = restart_whole_game(LEVELS)
    game_state = GameState.START
    collision_cell = None
    collision_until = 0
    flying_arrow = None
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game_state == GameState.START:
                    if START_BUTTON_RECT.collidepoint(event.pos):
                        current_level_index, board, remaining_mistakes, game_state = restart_whole_game(LEVELS)
                    continue

                if game_state == GameState.PLAYING:
                    if PREVIOUS_BUTTON_RECT.collidepoint(event.pos):
                        result = navigate_level(LEVELS, current_level_index, -1)
                        if result is not None:
                            current_level_index, board, remaining_mistakes, game_state = result
                            collision_cell = None
                            flying_arrow = None
                    elif NEXT_BUTTON_RECT.collidepoint(event.pos):
                        result = navigate_level(LEVELS, current_level_index, 1)
                        if result is not None:
                            current_level_index, board, remaining_mistakes, game_state = result
                            collision_cell = None
                            flying_arrow = None
                    elif ACTION_BUTTON_RECT.collidepoint(event.pos):
                        current_level_index, board, remaining_mistakes, game_state = restart_current_level(
                            LEVELS, current_level_index
                        )
                        collision_cell = None
                        flying_arrow = None
                    elif flying_arrow is None:
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
                                flying_arrow = FlyingArrow(
                                    previous_arrow, pygame.time.get_ticks(), FLYING_DURATION_MS
                                )
                elif ACTION_BUTTON_RECT.collidepoint(event.pos):
                    if game_state == GameState.PASSED and current_level_index < len(LEVELS) - 1:
                        current_level_index, board, remaining_mistakes, game_state = advance_level(
                            LEVELS, current_level_index
                        )
                    elif game_state == GameState.PASSED:
                        current_level_index, board, remaining_mistakes, game_state = restart_whole_game(LEVELS)
                    else:
                        current_level_index, board, remaining_mistakes, game_state = restart_current_level(
                            LEVELS, current_level_index
                        )
                    collision_cell = None
                    flying_arrow = None

        now = pygame.time.get_ticks()
        if flying_arrow is not None and now - flying_arrow.start_time >= flying_arrow.duration:
            flying_arrow = None
            game_state = state_after_successful_removal(board)
        if collision_cell is not None and now >= collision_until:
            collision_cell = None

        screen.fill(BACKGROUND_COLOR)
        if game_state == GameState.START:
            draw_start_screen(screen, title_font, font)
        else:
            draw_board(screen, board, collision_cell)
            if flying_arrow is not None:
                progress = min(1.0, (now - flying_arrow.start_time) / flying_arrow.duration)
                draw_flying_arrow(screen, flying_arrow, progress)
            level_title = title_font.render(
                f"第 {current_level_index + 1} / {len(LEVELS)} 关", True, TEXT_COLOR
            )
            screen.blit(level_title, level_title.get_rect(center=(WINDOW_WIDTH // 2, 28)))
            if game_state == GameState.PLAYING:
                chances = "● " * remaining_mistakes + "○ " * (3 - remaining_mistakes)
                chance_text = small_font.render(
                    f"剩余机会：{chances.strip()}", True, SUBTLE_TEXT_COLOR
                )
                screen.blit(chance_text, chance_text.get_rect(center=(WINDOW_WIDTH // 2, 78)))
                draw_button(screen, PREVIOUS_BUTTON_RECT, "上一关", small_font, current_level_index > 0)
                draw_button(screen, NEXT_BUTTON_RECT, "下一关", small_font, current_level_index < len(LEVELS) - 1)
                draw_button(screen, ACTION_BUTTON_RECT, "重新开始", small_font)
            elif game_state == GameState.PASSED:
                message = "全部通关！" if current_level_index == len(LEVELS) - 1 else "本关通过！"
                button = "重新挑战" if current_level_index == len(LEVELS) - 1 else "进入下一关"
                message_surface = font.render(message, True, TEXT_COLOR)
                screen.blit(message_surface, message_surface.get_rect(center=(WINDOW_WIDTH // 2, 78)))
                draw_button(screen, ACTION_BUTTON_RECT, button, small_font)
            else:
                message_surface = font.render("挑战失败", True, TEXT_COLOR)
                screen.blit(message_surface, message_surface.get_rect(center=(WINDOW_WIDTH // 2, 78)))
                draw_button(screen, ACTION_BUTTON_RECT, "重新开始", small_font)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
