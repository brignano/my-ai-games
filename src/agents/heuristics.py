"""
Simple heuristic agents for game environments.
"""


def flappy_heuristic(state):
    """
    Simple rule-based agent for Flappy Bird.
    
    Args:
        state: numpy array [bird_y_norm, bird_v_norm, pipe_dx_norm, gap_center_y_norm]
    
    Returns:
        action: 0 (no-op) or 1 (flap)
    
    Strategy:
        If the bird is below the gap center, flap.
        Otherwise, do nothing and let gravity bring it down.
    """
    bird_y_norm = state[0]
    gap_center_y_norm = state[3]
    
    # If bird is below the gap center, flap
    if bird_y_norm > gap_center_y_norm:
        return 1  # flap
    else:
        return 0  # no-op
