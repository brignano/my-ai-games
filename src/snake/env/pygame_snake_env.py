"""Gymnasium-compatible wrapper for Snake game."""
import gymnasium as gym
from gymnasium import spaces
import numpy as np
import random
from ..game import SnakeGame


class PygameSnakeEnv(gym.Env):
    """
    Gym environment wrapper for Snake game.
    
    Action space: Discrete(4) - [up, right, down, left]
    Observation space: Box(shape=(20, 20, 2), dtype=float32) - grid with snake and food channels
    """
    
    metadata = {"render_modes": []}
    
    def __init__(self):
        super().__init__()
        self.game = SnakeGame()
        
        # Action space: 4 discrete actions
        self.action_space = spaces.Discrete(4)
        
        # Observation space: (ROWS, COLS, 2) grid
        self.observation_space = spaces.Box(
            low=0.0,
            high=1.0,
            shape=(SnakeGame.ROWS, SnakeGame.COLS, 2),
            dtype=np.float32
        )
    
    def reset(self, seed=None, options=None):
        """Reset the environment."""
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        obs = self.game.reset()
        return obs, {}
    
    def step(self, action):
        """Take a step in the environment."""
        obs, reward, done, info = self.game.step(action)
        # Gymnasium expects (obs, reward, terminated, truncated, info)
        return obs, reward, done, False, info
    
    def render(self):
        """Render the current game state using Pygame."""
        import pygame
        if not hasattr(self, '_screen'):
            pygame.init()
            CELL = 20
            self._screen = pygame.display.set_mode((self.game.COLS * CELL, self.game.ROWS * CELL))
            self._clock = pygame.time.Clock()
            self._font = pygame.font.SysFont(None, 32)
            self._CELL = CELL
        screen = self._screen
        game = self.game
        CELL = self._CELL
        # Process events to keep window responsive
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                import sys
                sys.exit()
        # Colors
        BLACK = (0, 0, 0)
        GREEN = (0, 200, 0)
        RED = (200, 0, 0)
        BLUE = (50, 150, 255)
        WHITE = (255, 255, 255)
        # Draw background
        screen.fill(BLACK)
        # Draw food
        if game.food:
            fx, fy = game.food
            pygame.draw.rect(screen, RED, pygame.Rect(fx*CELL, fy*CELL, CELL, CELL))
        # Draw snake
        for i, (x, y) in enumerate(game.snake):
            color = GREEN if i == 0 else BLUE
            pygame.draw.rect(screen, color, pygame.Rect(x*CELL, y*CELL, CELL, CELL))
        # Draw score
        score_surf = self._font.render(f"Score: {game.score}", True, WHITE)
        screen.blit(score_surf, (5, 5))
        pygame.display.flip()
        self._clock.tick(10)
    
    def close(self):
        """Clean up resources."""
        pass
