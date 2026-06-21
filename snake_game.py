"""
Snake Game
----------
Classic Snake game built with Pygame.

Controls:
  Arrow keys / WASD - move
  P                 - pause / unpause
  R                 - restart after game over
  ESC               - quit

Run with:  python snake_game.py
"""

import pygame
import random
import sys

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
CELL_SIZE = 24
GRID_WIDTH = 25
GRID_HEIGHT = 20
WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT + 60  # extra space for score bar

FPS_START = 8          # initial snake speed (moves per second)
FPS_MAX = 18           # speed cap as the snake grows
SPEED_UP_EVERY = 5      # increase speed every N food eaten

# Colors
BG_COLOR = (24, 28, 36)
GRID_COLOR = (32, 37, 47)
SNAKE_HEAD_COLOR = (98, 209, 124)
SNAKE_BODY_COLOR = (61, 158, 88)
FOOD_COLOR = (235, 92, 92)
TEXT_COLOR = (235, 235, 235)
SHADOW_COLOR = (15, 17, 22)
PANEL_COLOR = (18, 21, 27)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
OPPOSITE = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}


class SnakeGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font_big = pygame.font.SysFont("arial", 44, bold=True)
        self.font_med = pygame.font.SysFont("arial", 24, bold=True)
        self.font_small = pygame.font.SysFont("arial", 18)
        self.high_score = 0
        self.reset()

    def reset(self):
        cx, cy = GRID_WIDTH // 2, GRID_HEIGHT // 2
        self.snake = [(cx - 1, cy), (cx - 2, cy), (cx - 3, cy)]
        self.direction = RIGHT
        self.pending_direction = RIGHT
        self.food = self.spawn_food()
        self.score = 0
        self.fps = FPS_START
        self.game_over = False
        self.paused = False
        self.eaten_count = 0

    def spawn_food(self):
        occupied = set(self.snake)
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if pos not in occupied:
                return pos

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.key in (pygame.K_UP, pygame.K_w):
                    self._try_set_direction(UP)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self._try_set_direction(DOWN)
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    self._try_set_direction(LEFT)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    self._try_set_direction(RIGHT)
                elif event.key == pygame.K_p and not self.game_over:
                    self.paused = not self.paused
                elif event.key == pygame.K_r and self.game_over:
                    self.reset()

    def _try_set_direction(self, new_dir):
        # Prevent reversing directly into the snake's own body
        if new_dir != OPPOSITE[self.direction]:
            self.pending_direction = new_dir

    def update(self):
        if self.game_over or self.paused:
            return

        self.direction = self.pending_direction
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        # Check wall collision
        if not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT):
            self.end_game()
            return

        # Check self collision
        if new_head in self.snake:
            self.end_game()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 10
            self.eaten_count += 1
            self.food = self.spawn_food()
            if self.eaten_count % SPEED_UP_EVERY == 0 and self.fps < FPS_MAX:
                self.fps += 1
        else:
            self.snake.pop()

    def end_game(self):
        self.game_over = True
        self.high_score = max(self.high_score, self.score)

    def draw_grid(self):
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                if (x + y) % 2 == 0:
                    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE + 60, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(self.screen, GRID_COLOR, rect)

    def draw_snake(self):
        for i, (x, y) in enumerate(self.snake):
            rect = pygame.Rect(x * CELL_SIZE + 1, y * CELL_SIZE + 60 + 1, CELL_SIZE - 2, CELL_SIZE - 2)
            color = SNAKE_HEAD_COLOR if i == 0 else SNAKE_BODY_COLOR
            pygame.draw.rect(self.screen, color, rect, border_radius=6)

    def draw_food(self):
        x, y = self.food
        cx = x * CELL_SIZE + CELL_SIZE // 2
        cy = y * CELL_SIZE + 60 + CELL_SIZE // 2
        pygame.draw.circle(self.screen, FOOD_COLOR, (cx, cy), CELL_SIZE // 2 - 3)

    def draw_panel(self):
        pygame.draw.rect(self.screen, PANEL_COLOR, (0, 0, WINDOW_WIDTH, 60))
        score_surf = self.font_med.render(f"Score: {self.score}", True, TEXT_COLOR)
        high_surf = self.font_small.render(f"Best: {self.high_score}", True, TEXT_COLOR)
        self.screen.blit(score_surf, (16, 16))
        self.screen.blit(high_surf, (WINDOW_WIDTH - high_surf.get_width() - 16, 22))

    def draw_centered_text(self, text, font, color, y_offset=0):
        surf = font.render(text, True, color)
        shadow = font.render(text, True, SHADOW_COLOR)
        x = WINDOW_WIDTH // 2 - surf.get_width() // 2
        y = WINDOW_HEIGHT // 2 - surf.get_height() // 2 + y_offset
        self.screen.blit(shadow, (x + 2, y + 2))
        self.screen.blit(surf, (x, y))

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.draw_grid()
        self.draw_food()
        self.draw_snake()
        self.draw_panel()

        if self.paused:
            self.draw_centered_text("PAUSED", self.font_big, TEXT_COLOR)
        elif self.game_over:
            self.draw_centered_text("GAME OVER", self.font_big, FOOD_COLOR, -20)
            self.draw_centered_text("Press R to restart", self.font_med, TEXT_COLOR, 30)

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(self.fps)


if __name__ == "__main__":
    SnakeGame().run()
