"""
Train a random agent in the Flappy Bird Gym environment (for demonstration).
"""

import os
import sys
from dotenv import load_dotenv
load_dotenv()
from src.flappy.env.pygame_flappy_env import PygameFlappyEnv
from src.flappy.agents.random_agent import RandomAgent

NUM_EPISODES = 5


def main():

    render = os.environ.get("RENDER") == "1" or "--render" in sys.argv
    env = PygameFlappyEnv()
    agent = RandomAgent(env.action_space)

    for episode in range(NUM_EPISODES):
        obs, info = env.reset()
        done = False
        total_reward = 0
        steps = 0

        while not done:
            action = agent.select_action(obs)
            obs, reward, done, truncated, info = env.step(action)
            agent.learn(obs, reward, done, info)  # No-op for random agent
            total_reward += reward
            steps += 1
            if render:
                env.render()

        print(f"Episode {episode+1}: steps={steps}, total_reward={total_reward}, info={info}")

    env.close()

if __name__ == "__main__":
    main()
