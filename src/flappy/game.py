"""
Flappy Bird Game class for programmatic interaction and RL training.
"""
import random
import numpy as np


# Constants from the original app
SCREEN_W, SCREEN_H = 400, 600
BIRD_X = 80
BIRD_RADIUS = 16
GRAVITY = 0.5
FLAP_STRENGTH = -9
PIPE_WIDTH = 70
GAP_SIZE = 160
PIPE_SPEED = 3


class FlappyGame:
    """
    A programmatic Flappy Bird game that can be used for RL training.
    
    The game returns observations as a state vector:
    [bird_y_norm, bird_v_norm, pipe_dx_norm, gap_center_y_norm]
    
    All values are normalized to roughly [-1, 1] or [0, 1] range.
    
    Actions:
    - 0: no-op (do nothing)
    - 1: flap
    
    Rewards:
    - +1 for passing through a pipe
    - -1 for collision
    - Small positive reward per frame survived
    """
    
    def __init__(self, screen_w=SCREEN_W, screen_h=SCREEN_H):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.bird_x = BIRD_X
        self.bird_radius = BIRD_RADIUS
        self.gravity = GRAVITY
        self.flap_strength = FLAP_STRENGTH
        self.pipe_width = PIPE_WIDTH
        self.gap_size = GAP_SIZE
        self.pipe_speed = PIPE_SPEED
        self.tick_count = 0
        self.pipe_spawn_interval = 90  # ticks (roughly 1.5 seconds at 60 FPS)
        self.reset()
    
    def reset(self):
        """Reset the game to initial state and return initial observation."""
        self.bird_y = self.screen_h / 2
        self.bird_v = 0.0
        self.pipes = []
        self.score = 0
        self.done = False
        self.tick_count = 0
        self.last_pipe_tick = 0
        return self._get_obs()
    
    def _new_pipe(self, x):
        """Create a new pipe at position x."""
        gap_y = random.randint(100, self.screen_h - 100 - self.gap_size)
        return {
            "x": x,
            "gap_y": gap_y,
            "gap_bottom": gap_y + self.gap_size,
            "passed": False
        }
    
    def _get_obs(self):
        """
        Return observation as a normalized state vector.
        [bird_y_norm, bird_v_norm, pipe_dx_norm, gap_center_y_norm]
        """
        # Normalize bird y position [0, 1]
        bird_y_norm = self.bird_y / self.screen_h
        
        # Normalize bird velocity (approximately [-1, 1])
        bird_v_norm = self.bird_v / 20.0  # typical max velocity ~20
        
        # Find the next pipe (first pipe that hasn't passed the bird)
        next_pipe = None
        for pipe in self.pipes:
            if pipe["x"] + self.pipe_width > self.bird_x:
                next_pipe = pipe
                break
        
        if next_pipe:
            # Distance to next pipe, normalized by screen width
            pipe_dx_norm = (next_pipe["x"] - self.bird_x) / self.screen_w
            # Gap center y position, normalized [0, 1]
            gap_center = (next_pipe["gap_y"] + next_pipe["gap_bottom"]) / 2
            gap_center_y_norm = gap_center / self.screen_h
        else:
            # No pipes yet, use default values
            pipe_dx_norm = 1.0
            gap_center_y_norm = 0.5
        
        return np.array([
            bird_y_norm, 
            bird_v_norm, 
            pipe_dx_norm, 
            gap_center_y_norm
        ], dtype=np.float32)
    
    def _check_collision(self):
        """Check if bird has collided with pipes or boundaries."""
        # Check ceiling and floor
        if self.bird_y - self.bird_radius <= 0 or self.bird_y + self.bird_radius >= self.screen_h:
            return True
        
        # Check pipe collision
        bird_left = self.bird_x - self.bird_radius
        bird_right = self.bird_x + self.bird_radius
        bird_top = self.bird_y - self.bird_radius
        bird_bottom = self.bird_y + self.bird_radius
        
        for pipe in self.pipes:
            pipe_left = pipe["x"]
            pipe_right = pipe["x"] + self.pipe_width
            
            # Check horizontal overlap
            if bird_right > pipe_left and bird_left < pipe_right:
                # Check if bird is in the gap
                if bird_top < pipe["gap_y"] or bird_bottom > pipe["gap_bottom"]:
                    return True
        
        return False
    
    def step(self, action):
        """
        Execute one step with the given action.
        
        Args:
            action (int): 0=no-op, 1=flap
        
        Returns:
            tuple: (observation, reward, done, info)
        """
        if self.done:
            return self._get_obs(), 0.0, True, {"score": self.score}
        
        # Apply action
        if action == 1:
            self.bird_v = self.flap_strength
        
        # Physics
        self.bird_v += self.gravity
        self.bird_y += self.bird_v
        
        # Update tick counter
        self.tick_count += 1
        
        # Spawn pipes at intervals
        if self.tick_count - self.last_pipe_tick >= self.pipe_spawn_interval:
            self.pipes.append(self._new_pipe(self.screen_w))
            self.last_pipe_tick = self.tick_count
        
        # Move pipes
        for pipe in self.pipes:
            pipe["x"] -= self.pipe_speed
        
        # Check for scoring and remove off-screen pipes
        reward = 0.01  # Small reward per frame survived
        for pipe in self.pipes:
            if not pipe["passed"] and pipe["x"] + self.pipe_width < self.bird_x:
                pipe["passed"] = True
                self.score += 1
                reward = 1.0  # Larger reward for passing a pipe
        
        self.pipes = [p for p in self.pipes if p["x"] + self.pipe_width > -50]
        
        # Check collision
        if self._check_collision():
            self.done = True
            reward = -1.0
            info = {"score": self.score, "reason": "collision"}
            return self._get_obs(), reward, True, info
        
        info = {"score": self.score}
        return self._get_obs(), reward, self.done, info
