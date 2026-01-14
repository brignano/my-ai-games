import numpy as np

class RandomAgent:
    """
    A simple agent that takes random actions from the environment's action space.
    """
    def __init__(self, action_space):
        self.action_space = action_space

    def select_action(self, observation):
        return self.action_space.sample()

    def learn(self, *args, **kwargs):
        pass  # No learning for random agent
