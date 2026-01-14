"""Gymnasium-compatible wrapper for Flappy Bird game."""
import gymnasium as gym
from gymnasium import spaces
import numpy as np
import random
from ..game import FlappyGame


class PygameFlappyEnv(gym.Env):
    """
    Gym environment wrapper for Flappy Bird game.
    
    Action space: Discrete(2) - [no-op, flap]
    Observation space: Box(shape=(4,), dtype=float32) - [bird_y, bird_v, pipe_dx, gap_center_y]
    """
    
    metadata = {"render_modes": []}
    
    def __init__(self):
        super().__init__()
        self.game = FlappyGame()
        
        # Action space: 2 discrete actions (no-op, flap)
        self.action_space = spaces.Discrete(2)
        
        # Observation space: 4D state vector
        self.observation_space = spaces.Box(
            low=-2.0,
            high=2.0,
            shape=(4,),
            dtype=np.float32
        )
    
    def reset(self, seed=None, options=None):
        """Reset the environment."""
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        obs = self.game.reset()
        return np.array(obs, dtype=np.float32), {}
    
    def step(self, action):
        """Take a step in the environment."""
        obs, reward, done, info = self.game.step(action)
        # Gymnasium expects (obs, reward, terminated, truncated, info)
        return np.array(obs, dtype=np.float32), reward, done, False, info
    
    def render(self):
        """Render the current game state using Pygame."""
        import pygame
        if not hasattr(self, '_screen'):
            pygame.init()
            self._screen = pygame.display.set_mode((self.game.SCREEN_W, self.game.SCREEN_H))
            self._clock = pygame.time.Clock()
            self._font = pygame.font.SysFont(None, 36)
        screen = self._screen
        game = self.game
        # Process events to keep window responsive
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                import sys
                sys.exit()
        # Colors
        SKY = (135, 206, 235)
        GREEN = (76, 187, 23)
        BLACK = (0, 0, 0)
        YELLOW = (255, 255, 0)
        # Draw background
        screen.fill(SKY)
        # Draw bird
        pygame.draw.circle(screen, BLACK, (game.BIRD_X, int(game.bird_y)), game.BIRD_RADIUS)
        pygame.draw.circle(screen, YELLOW, (game.BIRD_X, int(game.bird_y)), game.BIRD_RADIUS - 3)
        # Draw pipes
        for p in game.pipes:
            # Top pipe
            pygame.draw.rect(screen, GREEN, pygame.Rect(p["top_x"], 0, game.PIPE_WIDTH, p["top_h"]))
            # Bottom pipe
            pygame.draw.rect(screen, GREEN, pygame.Rect(p["bottom_x"], p["bottom_y"], game.PIPE_WIDTH, p["bottom_h"]))
        # Draw score
        score_surf = self._font.render(f"Score: {game.score}", True, BLACK)
        screen.blit(score_surf, (10, 10))
        pygame.display.flip()
        self._clock.tick(60)
    
    def close(self):
        """Clean up resources."""
        pass
