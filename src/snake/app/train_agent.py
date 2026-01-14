"""
Train a random agent in the Snake Gym environment (for demonstration).
"""
import os
import sys
from dotenv import load_dotenv
load_dotenv()
from src.snake.env.pygame_snake_env import PygameSnakeEnv

class RandomAgent:
    def __init__(self, action_space):
        self.action_space = action_space
    def select_action(self, observation):
        return self.action_space.sample()
    def learn(self, *args, **kwargs):
        pass

NUM_EPISODES = 5

def main():
    render = os.environ.get("RENDER") == "1" or "--render" in sys.argv
    env = PygameSnakeEnv()
    agent = RandomAgent(env.action_space)

    for episode in range(NUM_EPISODES):
        obs, info = env.reset()
        done = False
        total_reward = 0
        steps = 0

        while not done:
            action = agent.select_action(obs)
            obs, reward, done, truncated, info = env.step(action)
            agent.learn(obs, reward, done, info)
            total_reward += reward
            steps += 1
            if render:
                env.render()

        print(f"Episode {episode+1}: steps={steps}, total_reward={total_reward}, info={info}")

    env.close()

if __name__ == "__main__":
    main()
