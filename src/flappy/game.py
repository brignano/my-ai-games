"""
Flappy Bird game logic - programmatic API for RL training.
Returns observation, reward, done, info on each step.
"""
import random


class FlappyGame:
    """Flappy Bird game with reset() and step(action) interface."""
    
    # Game constants matching the app script
    SCREEN_W = 400
    SCREEN_H = 600
    BIRD_X = 80
    BIRD_RADIUS = 16
    GRAVITY = 0.5
    FLAP_STRENGTH = -9
    PIPE_WIDTH = 70
    GAP_SIZE = 160
    PIPE_SPEED = 3
    PIPE_INTERVAL_TICKS = 25  # ~1500ms at 60 FPS
    
    # Action mapping
    ACTION_NOOP = 0
    ACTION_FLAP = 1
    
    def __init__(self):
        self.bird_y = 0.0
        self.bird_v = 0.0
        self.pipes = []
        self.score = 0
        self.ticks = 0
        self.last_pipe_tick = 0
        self.done = False
        
    def reset(self):
        """Reset the game to initial state."""
        self.bird_y = self.SCREEN_H / 2
        self.bird_v = 0.0
        self.pipes = []
        self.score = 0
        self.ticks = 0
        self.last_pipe_tick = 0
        self.done = False
        return self._get_obs()
    
    def step(self, action):
        """
        Take one step in the game.
        
        Args:
            action: int, 0=no-op, 1=flap
        
        Returns:
            obs: numpy array [bird_y_norm, bird_v_norm, pipe_dx_norm, gap_center_y_norm]
            reward: float
            done: bool
            info: dict with score and ticks
        """
        if self.done:
            # Game already over
            return self._get_obs(), 0.0, True, {"score": self.score, "ticks": self.ticks}
        
        # Handle flap action
        if action == self.ACTION_FLAP:
            self.bird_v = self.FLAP_STRENGTH
        
        # Physics update
        self.bird_v += self.GRAVITY
        self.bird_y += self.bird_v
        
        # Pipe generation
        if self.ticks - self.last_pipe_tick >= self.PIPE_INTERVAL_TICKS:
            self.pipes.append(self._new_pipe(self.SCREEN_W))
            self.last_pipe_tick = self.ticks
        
        # Move pipes
        for p in self.pipes:
            p["top_x"] -= self.PIPE_SPEED
            p["bottom_x"] -= self.PIPE_SPEED
        
        # Score and remove offscreen pipes
        reward = 0.01  # small positive reward for surviving
        for p in self.pipes:
            if not p["passed"] and p["top_x"] + self.PIPE_WIDTH < self.BIRD_X:
                p["passed"] = True
                self.score += 1
                reward = 1.0  # scored a point
        
        self.pipes = [p for p in self.pipes if p["top_x"] + self.PIPE_WIDTH > -50]
        
        # Check collision
        if self._collided():
            self.done = True
            reward = -1.0  # collision penalty
        
        self.ticks += 1
        obs = self._get_obs()
        info = {"score": self.score, "ticks": self.ticks}
        
        return obs, reward, self.done, info
    
    def _get_obs(self):
        """
        Return state-based observation as a 1D vector:
        [bird_y_norm, bird_v_norm, pipe_dx_norm, gap_center_y_norm]
        
        All values normalized to roughly [-1, 1] range.
        """
        # Normalize bird position and velocity
        bird_y_norm = (self.bird_y - self.SCREEN_H / 2) / (self.SCREEN_H / 2)
        bird_v_norm = self.bird_v / 10.0  # arbitrary scaling
        
        # Find the next pipe (first pipe to the right of bird)
        next_pipe = None
        for p in self.pipes:
            if p["top_x"] + self.PIPE_WIDTH >= self.BIRD_X:
                next_pipe = p
                break
        
        if next_pipe:
            # Distance to pipe
            pipe_dx = next_pipe["top_x"] - self.BIRD_X
            pipe_dx_norm = pipe_dx / self.SCREEN_W
            
            # Gap center
            gap_center = next_pipe["gap_y"] + self.GAP_SIZE / 2
            gap_center_norm = (gap_center - self.SCREEN_H / 2) / (self.SCREEN_H / 2)
        else:
            # No pipes ahead - use defaults
            pipe_dx_norm = 1.0
            gap_center_norm = 0.0
        
        return [bird_y_norm, bird_v_norm, pipe_dx_norm, gap_center_norm]
    
    def _new_pipe(self, x):
        """Create a new pipe at position x."""
        gap_y = random.randint(100, self.SCREEN_H - 100 - self.GAP_SIZE)
        return {
            "top_x": x,
            "top_y": 0,
            "top_h": gap_y,
            "bottom_x": x,
            "bottom_y": gap_y + self.GAP_SIZE,
            "bottom_h": self.SCREEN_H - (gap_y + self.GAP_SIZE),
            "gap_y": gap_y,
            "passed": False
        }
    
    def _collided(self):
        """Check if bird collided with pipes or boundaries."""
        # Check ceiling/floor
        if self.bird_y - self.BIRD_RADIUS <= 0 or self.bird_y + self.BIRD_RADIUS >= self.SCREEN_H:
            return True
        
        # Check pipe collision (simplified rectangular collision)
        bird_left = self.BIRD_X - self.BIRD_RADIUS
        bird_right = self.BIRD_X + self.BIRD_RADIUS
        bird_top = self.bird_y - self.BIRD_RADIUS
        bird_bottom = self.bird_y + self.BIRD_RADIUS
        
        for p in self.pipes:
            pipe_left = p["top_x"]
            pipe_right = p["top_x"] + self.PIPE_WIDTH
            
            # Check horizontal overlap
            if bird_right > pipe_left and bird_left < pipe_right:
                # Check vertical collision with top or bottom pipe
                if bird_top < p["top_h"] or bird_bottom > p["bottom_y"]:
                    return True
        
        return False
