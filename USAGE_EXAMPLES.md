# Gym Environment Usage Examples

This document shows how to use the new Gym-compatible environments for Snake and Flappy Bird.

## Installation

```bash
pip install -r requirements.txt
```

## Snake Environment

```python
from src.snake.env.pygame_snake_env import PygameSnakeEnv

# Create environment
env = PygameSnakeEnv()

# Reset to get initial observation
obs, info = env.reset()
print(f"Observation shape: {obs.shape}")  # (20, 20, 2)

# Take actions
for _ in range(100):
    action = env.action_space.sample()  # Random action
    obs, reward, done, truncated, info = env.step(action)
    if done:
        print(f"Game over! Score: {info['score']}")
        break
```

### Action Space
- 0: Up
- 1: Right
- 2: Down
- 3: Left

### Observation Space
- Shape: (20, 20, 2)
- Channel 0: Snake body (1 where snake is, 0 elsewhere)
- Channel 1: Food location (1 where food is, 0 elsewhere)

### Rewards
- +1.0: Ate food
- -1.0: Collision (wall or self)
- -0.01: Each step (encourages efficiency)

## Flappy Bird Environment

```python
from src.flappy.env.pygame_flappy_env import PygameFlappyEnv
from src.agents.heuristics import flappy_heuristic

# Create environment
env = PygameFlappyEnv()

# Reset
obs, info = env.reset()

# Use heuristic agent
for _ in range(1000):
    action = flappy_heuristic(obs)
    obs, reward, done, truncated, info = env.step(action)
    if done:
        print(f"Game over! Score: {info['score']}")
        break
```

### Action Space
- 0: No-op (do nothing)
- 1: Flap

### Observation Space
- Shape: (4,)
- [0]: bird_y_norm (normalized bird Y position)
- [1]: bird_v_norm (normalized bird vertical velocity)
- [2]: pipe_dx_norm (normalized distance to next pipe)
- [3]: gap_center_y_norm (normalized gap center Y position)

### Rewards
- +1.0: Passed a pipe
- -1.0: Collision
- +0.01: Each step survived

## Training with Stable-Baselines3

```python
from stable_baselines3 import PPO
from src.snake.env.pygame_snake_env import PygameSnakeEnv

# Create environment
env = PygameSnakeEnv()

# Train agent
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=100000)

# Save model
model.save("snake_ppo")

# Test trained agent
obs, info = env.reset()
for _ in range(1000):
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, done, truncated, info = env.step(action)
    if done:
        print(f"Score: {info['score']}")
        break
```

## Using the Original Game Scripts

The original game scripts still work as before when run directly:

```bash
python src/snake/app/snake.py
python src/flappy/app/flappy_bird.py
```

They can now also be imported without opening pygame windows, enabling headless training.
