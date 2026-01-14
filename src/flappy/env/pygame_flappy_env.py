"""Gymnasium-compatible wrapper for Flappy Bird game."""
import gymnasium as gym
from gymnasium import spaces
import numpy as np
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
            np.random.seed(seed)
        obs = self.game.reset()
        return np.array(obs, dtype=np.float32), {}
    
    def step(self, action):
        """Take a step in the environment."""
        obs, reward, done, info = self.game.step(action)
        # Gymnasium expects (obs, reward, terminated, truncated, info)
        return np.array(obs, dtype=np.float32), reward, done, False, info
    
    def render(self):
        """Rendering not implemented for headless training."""
        pass
    
    def close(self):
        """Clean up resources."""
        pass
