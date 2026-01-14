import pygame
import random
import sys

# Constants
CELL = 20
COLS, ROWS = 20, 20
SCREEN_W, SCREEN_H = COLS * CELL, ROWS * CELL
FPS = 10

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (50, 150, 255)

def random_cell(exclude):
    while True:
        p = (random.randrange(COLS), random.randrange(ROWS))
        if p not in exclude:
            return p

def draw_rect(screen, pos, color):
    x, y = pos
    pygame.draw.rect(screen, color, pygame.Rect(x*CELL, y*CELL, CELL, CELL))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 32)
    
    running = True
    snake = [(COLS//2, ROWS//2), (COLS//2 - 1, ROWS//2), (COLS//2 - 2, ROWS//2)]
    direction = (1, 0)  # moving right
    food = random_cell(snake)
    score = 0
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_over:
                    # restart
                    snake = [(COLS//2, ROWS//2), (COLS//2 - 1, ROWS//2), (COLS//2 - 2, ROWS//2)]
                    direction = (1, 0)
                    food = random_cell(snake)
                    score = 0
                    game_over = False
                if not game_over:
                    if event.key in (pygame.K_UP, pygame.K_w) and direction != (0, 1):
                        direction = (0, -1)
                    elif event.key in (pygame.K_DOWN, pygame.K_s) and direction != (0, -1):
                        direction = (0, 1)
                    elif event.key in (pygame.K_LEFT, pygame.K_a) and direction != (1, 0):
                        direction = (-1, 0)
                    elif event.key in (pygame.K_RIGHT, pygame.K_d) and direction != (-1, 0):
                        direction = (1, 0)

        if not game_over:
            # move
            head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
            # check collisions
            if (head[0] < 0 or head[0] >= COLS or head[1] < 0 or head[1] >= ROWS) or (head in snake):
                game_over = True
            else:
                snake.insert(0, head)
                if head == food:
                    score += 1
                    food = random_cell(snake)
                else:
                    snake.pop()

        # draw
        screen.fill(BLACK)
        draw_rect(screen, food, RED)
        for i, s in enumerate(snake):
            color = GREEN if i == 0 else BLUE
            draw_rect(screen, s, color)

        score_surf = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_surf, (5, 5))

        if game_over:
            go = font.render("Game Over - Press R to restart", True, WHITE)
            rect = go.get_rect(center=(SCREEN_W//2, SCREEN_H//2))
            screen.blit(go, rect)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()