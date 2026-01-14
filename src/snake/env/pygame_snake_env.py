"""Gymnasium-compatible wrapper for Snake game."""
import gymnasium as gym
from gymnasium import spaces
import numpy as np
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
            np.random.seed(seed)
        obs = self.game.reset()
        return obs, {}
    
    def step(self, action):
        """Take a step in the environment."""
        obs, reward, done, info = self.game.step(action)
        # Gymnasium expects (obs, reward, terminated, truncated, info)
        return obs, reward, done, False, info
    
    def render(self):
        """Rendering not implemented for headless training."""
        pass
    
    def close(self):
        """Clean up resources."""
        pass
