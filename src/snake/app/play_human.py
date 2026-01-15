import pygame
import sys
import numpy as np
from src.snake.game import SnakeGame

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (50, 150, 255)

CELL = 20
SCREEN_W, SCREEN_H = SnakeGame.COLS * CELL, SnakeGame.ROWS * CELL
FPS = 10

def draw_board(screen, game):
    obs = game._get_obs()
    # Draw food
    food_pos = np.argwhere(obs[:,:,1] == 1)
    for fy, fx in food_pos:
        pygame.draw.rect(screen, RED, pygame.Rect(fx*CELL, fy*CELL, CELL, CELL))
    # Draw snake
    snake_pos = np.argwhere(obs[:,:,0] == 1)
    for i, (sy, sx) in enumerate(snake_pos):
        color = GREEN if i == 0 else BLUE
        pygame.draw.rect(screen, color, pygame.Rect(sx*CELL, sy*CELL, CELL, CELL))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 32)

    running = True
    game = SnakeGame()
    obs = game.reset()

    direction = SnakeGame.ACTION_RIGHT

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game.done:
                    obs = game.reset()
                    direction = SnakeGame.ACTION_RIGHT
                if not game.done:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        direction = SnakeGame.ACTION_UP
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        direction = SnakeGame.ACTION_DOWN
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        direction = SnakeGame.ACTION_LEFT
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        direction = SnakeGame.ACTION_RIGHT

        if not game.done:
            obs, reward, done, info = game.step(direction)

        # draw
        screen.fill(BLACK)
        draw_board(screen, game)

        score_surf = font.render(f"Score: {game.score}", True, WHITE)
        screen.blit(score_surf, (5, 5))

        if game.done:
            go = font.render("Game Over - Press R to restart", True, WHITE)
            rect = go.get_rect(center=(SCREEN_W//2, SCREEN_H//2))
            screen.blit(go, rect)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()