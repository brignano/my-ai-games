"""
Train a random agent in the Flappy Bird Gym environment (for demonstration).
"""


def get_agent_class(name):
    if name == "random":
        from src.flappy.agents.random_agent import RandomAgent
        return RandomAgent
    elif name == "heuristic":
        from src.flappy.agents.heuristic_agent import HeuristicAgent
        return HeuristicAgent
    else:
        raise ValueError(f"Unknown agent: {name}")


def main():
    import argparse
    import os
    from src.flappy.env.pygame_flappy_env import PygameFlappyEnv
    from dotenv import load_dotenv
    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument("--agent", type=str, default=os.environ.get("AGENT",
                        "random"), help="Agent to use: random or heuristic")
    parser.add_argument("--render", action="store_true",
                        help="Render the environment")
    parser.add_argument("--episodes", type=int, default=int(
        os.environ.get("NUM_EPISODES", 5)), help="Number of episodes to run")
    args = parser.parse_args()

    render = os.environ.get("RENDER") == "1" or args.render
    env = PygameFlappyEnv()

    AgentClass = get_agent_class(args.agent)
    agent = AgentClass(env.action_space)

    for episode in range(args.episodes):
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
    main()
