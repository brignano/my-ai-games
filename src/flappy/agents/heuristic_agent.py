import random
from src.common.agent import Agent

class HeuristicAgent(Agent):
    """
    A simple heuristic agent for Flappy Bird:
    - Flap if the bird is below the center of the next pipe gap.
    - Otherwise, do nothing.
    """
    def __init__(self, action_space):
        super().__init__(action_space)

    def select_action(self, obs):
        # obs: [bird_y_norm, bird_v_norm, pipe_dx_norm, gap_center_y_norm]
        bird_y = obs[0]
        gap_center = obs[3]
        # Flap if bird is below the gap center
        if bird_y < gap_center:
            return 1  # Flap
        else:
            return 0  # No-op

    def learn(self, *args, **kwargs):
        pass  # No learning for heuristic agent
