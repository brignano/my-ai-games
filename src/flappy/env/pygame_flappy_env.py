"""
Gymnasium environment wrapper for Flappy Bird game.
"""
import gymnasium as gym
from gymnasium import spaces
import numpy as np

from ..game import FlappyGame


class PygameFlappyEnv(gym.Env):
    """
    Gymnasium environment wrapper for the Flappy Bird game.
    
    Observation Space: Box((4,)) - [bird_y_norm, bird_v_norm, pipe_dx_norm, gap_center_y_norm]
    Action Space: Discrete(2) - [0=no-op, 1=flap]
    
    Rewards:
    - +1 for passing through a pipe
    - -1 for collision
    - +0.01 per frame survived
    """
    
    metadata = {"render_modes": ["human"], "render_fps": 60}
    
    def __init__(self, render_mode=None):
        super().__init__()
        
        self.render_mode = render_mode
        
        # Initialize the game
        self.game = FlappyGame()
        
        # Define action and observation spaces
        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Box(
            low=np.array([-1.0, -1.0, 0.0, 0.0], dtype=np.float32),
            high=np.array([1.0, 1.0, 1.0, 1.0], dtype=np.float32),
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
