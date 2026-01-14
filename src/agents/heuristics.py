"""Simple heuristic agents for games."""


def flappy_heuristic(state):
    """
    Simple rule-based agent for Flappy Bird.
    
    Args:
        state: observation from FlappyGame, format:
               [bird_y_norm, bird_v_norm, pipe_dx_norm, gap_center_y_norm]
    
    Returns:
        action: 0 (no-op) or 1 (flap)
    
    Strategy:
        - If bird is below the gap center, flap
        - Otherwise, don't flap
    """
    bird_y_norm = state[0]
    gap_center_y_norm = state[3]
    
    # Flap if bird is below the gap center
    if bird_y_norm > gap_center_y_norm:
        return 1  # flap
    else:
        return 0  # no-op
