import pygame
import sys
from src.flappy.game import FlappyGame

# Colors
WHITE = (255, 255, 255)
SKY = (135, 206, 235)
GREEN = (76, 187, 23)
BLACK = (0, 0, 0)


def draw_bird(screen, game):
    pygame.draw.circle(screen, BLACK, (game.BIRD_X,
                       int(game.bird_y)), game.BIRD_RADIUS)
    pygame.draw.circle(screen, (255, 255, 0), (game.BIRD_X,
                       int(game.bird_y)), game.BIRD_RADIUS - 3)


def draw_pipes(screen, game):
    for p in game.pipes:
        # Top pipe
        pygame.draw.rect(screen, GREEN, pygame.Rect(
            p["top_x"], 0, game.PIPE_WIDTH, p["top_h"]))
        # Bottom pipe
        pygame.draw.rect(screen, GREEN, pygame.Rect(
            p["bottom_x"], p["bottom_y"], game.PIPE_WIDTH, p["bottom_h"]))


def main():
    pygame.init()
    screen = pygame.display.set_mode(
        (FlappyGame.SCREEN_W, FlappyGame.SCREEN_H))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    FPS = 60

    running = True
    game = FlappyGame()
    obs = game.reset()
    game_over = False

    while running:
        dt = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game.done:
                        obs = game.reset()
                    else:
                        obs, reward, done, info = game.step(
                            FlappyGame.ACTION_FLAP)
                if event.key == pygame.K_ESCAPE:
                    running = False

        if not game.done:
            obs, reward, done, info = game.step(FlappyGame.ACTION_NOOP)

        # drawing
        screen.fill(SKY)
        draw_bird(screen, game)
        draw_pipes(screen, game)

        score_surf = font.render(f"Score: {game.score}", True, BLACK)
        screen.blit(score_surf, (10, 10))

        if game.done:
            go = font.render("Game Over - Press SPACE to restart", True, BLACK)
            rect = go.get_rect(
                center=(FlappyGame.SCREEN_W//2, FlappyGame.SCREEN_H//2))
            screen.blit(go, rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

def draw_pipes(pipes):
    for p in pipes:
        pygame.draw.rect(screen, GREEN, p["top"])
        pygame.draw.rect(screen, GREEN, p["bottom"])

def collided(bird_y, pipes):
    bird_rect = pygame.Rect(BIRD_X - BIRD_RADIUS, bird_y - BIRD_RADIUS, BIRD_RADIUS*2, BIRD_RADIUS*2)
    if bird_y - BIRD_RADIUS <= 0 or bird_y + BIRD_RADIUS >= SCREEN_H:
        return True
    for p in pipes:
        if bird_rect.colliderect(p["top"]) or bird_rect.colliderect(p["bottom"]):
            return True
    return False

def main():
    global screen, clock, font
    
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    
    running = True
    bird_y = SCREEN_H // 2
    bird_v = 0.0
    pipes = []
    score = 0
    last_pipe = pygame.time.get_ticks()
    game_over = False

    while running:
        dt = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_over:
                        # restart
                        bird_y = SCREEN_H // 2
                        bird_v = 0.0
                        pipes = []
                        score = 0
                        last_pipe = pygame.time.get_ticks()
                        game_over = False
                    else:
                        bird_v = FLAP_STRENGTH
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not game_over:
                    bird_v = FLAP_STRENGTH

        if not game_over:
            # physics
            bird_v += GRAVITY
            bird_y += bird_v

            # pipes
            now = pygame.time.get_ticks()
            if now - last_pipe > PIPE_INTERVAL:
                pipes.append(new_pipe(SCREEN_W))
                last_pipe = now

            for p in pipes:
                p["top"].x -= PIPE_SPEED
                p["bottom"].x -= PIPE_SPEED

            # score and remove offscreen
            for p in pipes:
                if not p["passed"] and p["top"].x + PIPE_WIDTH < BIRD_X:
                    p["passed"] = True
                    score += 1
            pipes = [p for p in pipes if p["top"].right > -50]

            if collided(bird_y, pipes):
                game_over = True

        # drawing
        screen.fill(SKY)
        draw_bird(bird_y)
        draw_pipes(pipes)

        score_surf = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_surf, (10, 10))

        if game_over:
            go = font.render("Game Over - Press SPACE to restart", True, BLACK)
            rect = go.get_rect(center=(SCREEN_W//2, SCREEN_H//2))
            screen.blit(go, rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()