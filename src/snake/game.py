"""
Snake game logic - programmatic API for RL training.
Returns observation, reward, done, info on each step.
"""
import random
import numpy as np


class SnakeGame:
    """Snake game with reset() and step(action) interface."""
    
    # Game constants matching the app script
    COLS = 20
    ROWS = 20
    
    # Action mapping
    ACTION_UP = 0
    ACTION_RIGHT = 1
    ACTION_DOWN = 2
    ACTION_LEFT = 3
    
    def __init__(self):
        self.snake = []
        self.direction = (1, 0)  # (dx, dy)
        self.food = None
        self.score = 0
        self.steps = 0
        self.done = False
        
    def reset(self):
        """Reset the game to initial state."""
        # Start with 3-segment snake in the middle
        mid_x, mid_y = self.COLS // 2, self.ROWS // 2
        self.snake = [(mid_x, mid_y), (mid_x - 1, mid_y), (mid_x - 2, mid_y)]
        self.direction = (1, 0)  # moving right
        self.food = self._random_cell(exclude=self.snake)
        self.score = 0
        self.steps = 0
        self.done = False
        return self._get_obs()
    
    def step(self, action):
        """
        Take one step in the game.
        
        Args:
            action: int in [0, 1, 2, 3] = [up, right, down, left]
        
        Returns:
            obs: numpy array of shape (ROWS, COLS, 2) with channels [snake, food]
            reward: float
            done: bool
            info: dict with score and steps
        """
        if self.done:
            # Game already over, just return current state
            return self._get_obs(), 0.0, True, {"score": self.score, "steps": self.steps}
        
        # Map action to direction, but prevent 180-degree turns
        new_direction = self._action_to_direction(action)
        # Only change direction if it's not opposite to current direction
        if not (new_direction[0] == -self.direction[0] and new_direction[1] == -self.direction[1]):
            self.direction = new_direction
        
        # Move snake
        head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])
        
        # Check collisions
        reward = -0.01  # small negative reward per step to encourage efficiency
        if self._is_collision(head):
            self.done = True
            reward = -1.0  # collision penalty
        else:
            self.snake.insert(0, head)
            if head == self.food:
                # Ate food
                self.score += 1
                reward = 1.0  # food reward
                self.food = self._random_cell(exclude=self.snake)
            else:
                # Normal move - remove tail
                self.snake.pop()
        
        self.steps += 1
        obs = self._get_obs()
        info = {"score": self.score, "steps": self.steps}
        
        return obs, reward, self.done, info
    
    def _get_obs(self):
        """
        Return observation as a (ROWS, COLS, 2) numpy array.
        Channel 0: snake body (1 where snake is, 0 elsewhere)
        Channel 1: food location (1 where food is, 0 elsewhere)
        """
        obs = np.zeros((self.ROWS, self.COLS, 2), dtype=np.float32)
        
        # Mark snake positions
        for x, y in self.snake:
            if 0 <= x < self.COLS and 0 <= y < self.ROWS:
                obs[y, x, 0] = 1.0
        
        # Mark food position
        if self.food:
            fx, fy = self.food
            if 0 <= fx < self.COLS and 0 <= fy < self.ROWS:
                obs[fy, fx, 1] = 1.0
        
        return obs
    
    def _action_to_direction(self, action):
        """Convert discrete action to direction tuple."""
        if action == self.ACTION_UP:
            return (0, -1)
        elif action == self.ACTION_RIGHT:
            return (1, 0)
        elif action == self.ACTION_DOWN:
            return (0, 1)
        elif action == self.ACTION_LEFT:
            return (-1, 0)
        else:
            # Default to current direction if invalid action
            return self.direction
    
    def _is_collision(self, pos):
        """Check if position is a collision (wall or self)."""
        x, y = pos
        # Wall collision
        if x < 0 or x >= self.COLS or y < 0 or y >= self.ROWS:
            return True
        # Self collision
        if pos in self.snake:
            return True
        return False
    
    def _random_cell(self, exclude):
        """Generate random cell not in exclude list."""
        while True:
            p = (random.randrange(self.COLS), random.randrange(self.ROWS))
            if p not in exclude:
                return p
