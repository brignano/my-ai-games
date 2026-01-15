from abc import ABC, abstractmethod

class Agent(ABC):
    """
    Abstract base class for all agents in any game.
    Agents must implement select_action and learn methods.
    """
    def __init__(self, action_space):
        self.action_space = action_space

    @abstractmethod
    def select_action(self, obs):
        """Given an observation, select an action."""
        pass

    @abstractmethod
    def learn(self, *args, **kwargs):
        """Optional: update agent based on experience (can be a no-op)."""
        pass
