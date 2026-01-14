"""
Gymnasium environment wrapper for Snake game.
"""
import gymnasium as gym
from gymnasium import spaces
import numpy as np

from ..game import SnakeGame


class PygameSnakeEnv(gym.Env):
    """
    Gymnasium environment wrapper for the Snake game.
    
    Observation Space: Box((rows, cols, 2)) - grid with snake and food channels
    Action Space: Discrete(4) - [0=up, 1=right, 2=down, 3=left]
    
    Rewards:
    - +1 for eating food
    - -1 for collision
    - -0.01 per step
    """
    
    metadata = {"render_modes": ["human"], "render_fps": 10}
    
    def __init__(self, cols=20, rows=20, render_mode=None):
        super().__init__()
        
        self.cols = cols
        self.rows = rows
        self.render_mode = render_mode
        
        # Initialize the game
        self.game = SnakeGame(cols=cols, rows=rows)
        
        # Define action and observation spaces
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(
            low=0, high=1, 
            shape=(rows, cols, 2), 
            dtype=np.float32
        )
    
    def reset(self, seed=None, options=None):
        """Reset the environment and return initial observation."""
        super().reset(seed=seed)
        
        if seed is not None:
            np.random.seed(seed)
        
        obs = self.game.reset()
        info = {"score": self.game.score}
        
        return obs, info
    
    def step(self, action):
        """Execute one step in the environment."""
        obs, reward, done, info = self.game.step(action)
        terminated = done
        truncated = False
        
        return obs, reward, terminated, truncated, info
    
    def render(self):
        """Render the environment (not implemented for headless mode)."""
        if self.render_mode == "human":
            # Could implement pygame rendering here if needed
            pass
    
    def close(self):
        """Clean up resources."""
        pass
