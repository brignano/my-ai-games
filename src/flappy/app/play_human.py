import pygame
import random
import sys

# Game constants
SCREEN_W, SCREEN_H = 400, 600
FPS = 60

# Bird properties
BIRD_X = 80
BIRD_RADIUS = 16
GRAVITY = 0.5
FLAP_STRENGTH = -9

# Pipe properties
PIPE_WIDTH = 70
GAP_SIZE = 160
PIPE_SPEED = 3
PIPE_INTERVAL = 1500  # ms

# Colors
WHITE = (255, 255, 255)
SKY = (135, 206, 235)
GREEN = (76, 187, 23)
BLACK = (0, 0, 0)

# Global variables for pygame objects (initialized in main)
screen = None
clock = None
font = None

def new_pipe(x):
    gap_y = random.randint(100, SCREEN_H - 100 - GAP_SIZE)
    top = pygame.Rect(x, 0, PIPE_WIDTH, gap_y)
    bottom = pygame.Rect(x, gap_y + GAP_SIZE, PIPE_WIDTH, SCREEN_H - (gap_y + GAP_SIZE))
    return {"top": top, "bottom": bottom, "passed": False}

def draw_bird(y):
    pygame.draw.circle(screen, BLACK, (BIRD_X, int(y)), BIRD_RADIUS)
    pygame.draw.circle(screen, (255,255,0), (BIRD_X, int(y)), BIRD_RADIUS - 3)  # inner

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