"""
Run the Snake Gym environment with a random agent (headless, prints episode summary).
"""
from src.snake.env.pygame_snake_env import PygameSnakeEnv

def main():
    env = PygameSnakeEnv()
    obs, info = env.reset()
    done = False
    total_reward = 0
    steps = 0

    while not done:
        action = env.action_space.sample()  # random action
        obs, reward, done, truncated, info = env.step(action)
        total_reward += reward
        steps += 1

    print(f"Episode finished in {steps} steps, total reward: {total_reward}, info: {info}")
    env.close()

if __name__ == "__main__":
    main()
