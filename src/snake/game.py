"""
Snake Game class for programmatic interaction and RL training.
"""
import random
import numpy as np


# Constants from the original app
COLS, ROWS = 20, 20


class SnakeGame:
    """
    A programmatic Snake game that can be used for RL training.
    
    The game returns observations as a (rows, cols, 2) grid where:
    - Channel 0: snake body (1 for snake cells, 0 otherwise)
    - Channel 1: food location (1 for food cell, 0 otherwise)
    
    Actions are discrete:
    - 0: up
    - 1: right
    - 2: down
    - 3: left
    
    Rewards:
    - +1 for eating food
    - -1 for collision (wall or self)
    - -0.01 per step (to encourage efficiency)
    """
    
    # Reward constants
    FOOD_REWARD = 1.0
    COLLISION_PENALTY = -1.0
    STEP_PENALTY = -0.01
    
    def __init__(self, cols=COLS, rows=ROWS):
        self.cols = cols
        self.rows = rows
        self.reset()
    
    def reset(self):
        """Reset the game to initial state and return initial observation."""
        # Initial snake: 3 cells in the middle, moving right
        mid_x, mid_y = self.cols // 2, self.rows // 2
        self.snake = [(mid_x, mid_y), (mid_x - 1, mid_y), (mid_x - 2, mid_y)]
        self.direction = (1, 0)  # moving right
        self.food = self._random_cell(self.snake)
        self.score = 0
        self.done = False
        return self._get_obs()
    
    def _random_cell(self, exclude):
        """Generate a random cell position not in the exclude list."""
        # For efficiency when board is nearly full, use a different strategy
        if len(exclude) > self.cols * self.rows * 0.75:
            # If more than 75% full, find all empty cells
            all_cells = [(x, y) for x in range(self.cols) for y in range(self.rows)]
            empty_cells = [cell for cell in all_cells if cell not in exclude]
            if empty_cells:
                return random.choice(empty_cells)
            # Fallback if no empty cells (game should be over)
            return (0, 0)
        
        # For normal play, random sampling is faster
        max_attempts = 1000  # Prevent infinite loops
        for _ in range(max_attempts):
            p = (random.randrange(self.cols), random.randrange(self.rows))
            if p not in exclude:
                return p
        
        # Fallback: find first empty cell
        for x in range(self.cols):
            for y in range(self.rows):
                if (x, y) not in exclude:
                    return (x, y)
        return (0, 0)  # Should never reach here in normal gameplay
    
    def _get_obs(self):
        """
        Return observation as a (rows, cols, 2) numpy array.
        Channel 0: snake body
        Channel 1: food location
        """
        obs = np.zeros((self.rows, self.cols, 2), dtype=np.float32)
        
        # Mark snake positions in channel 0
        for x, y in self.snake:
            if 0 <= x < self.cols and 0 <= y < self.rows:
                obs[y, x, 0] = 1.0
        
        # Mark food position in channel 1
        fx, fy = self.food
        if 0 <= fx < self.cols and 0 <= fy < self.rows:
            obs[fy, fx, 1] = 1.0
        
        return obs
    
    def step(self, action):
        """
        Execute one step with the given action.
        
        Args:
            action (int): 0=up, 1=right, 2=down, 3=left
        
        Returns:
            tuple: (observation, reward, done, info)
        """
        if self.done:
            # If game is over, return current state
            return self._get_obs(), 0.0, True, {"score": self.score}
        
        # Map action to direction, but don't allow reversing
        action_to_direction = {
            0: (0, -1),  # up
            1: (1, 0),   # right
            2: (0, 1),   # down
            3: (-1, 0),  # left
        }
        
        new_direction = action_to_direction.get(action, self.direction)
        
        # Prevent reversing direction (can't go opposite to current direction)
        # If the new direction is opposite, the sum would be (0, 0)
        if not (new_direction[0] + self.direction[0] == 0 and 
                new_direction[1] + self.direction[1] == 0):
            self.direction = new_direction
        
        # Move the snake
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        
        # Check for collisions
        hit_wall = (new_head[0] < 0 or new_head[0] >= self.cols or 
                   new_head[1] < 0 or new_head[1] >= self.rows)
        hit_self = new_head in self.snake
        
        if hit_wall or hit_self:
            self.done = True
            reward = self.COLLISION_PENALTY
            info = {"score": self.score, "reason": "collision"}
            return self._get_obs(), reward, True, info
        
        # Move snake
        self.snake.insert(0, new_head)
        
        # Check if food was eaten
        if new_head == self.food:
            self.score += 1
            self.food = self._random_cell(self.snake)
            reward = self.FOOD_REWARD
        else:
            # Remove tail if no food eaten
            self.snake.pop()
            reward = self.STEP_PENALTY
        
        info = {"score": self.score}
        return self._get_obs(), reward, self.done, info
