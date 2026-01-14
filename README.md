# my-ai-games

A collection of AI-powered games and experiments.


## Project Structure

```
my-ai-games/
├─ README.md
├─ .gitignore
├─ pyproject.toml / requirements.txt
├─ src/
│  ├─ common/                # utilities: screen capture, wrappers, net utils
│  ├─ flappy/                # flappy bot & experiments
│  │  ├─ app/                # scripts to run the game / bot
│  │  ├─ src/                # code for the bot or env
│  │  └─ configs/
│  └─ snake/                 # snake environment & RL training
│     ├─ env/                # Gym env implementation
│     ├─ train/              # training scripts & configs
│     └─ configs/
├─ notebooks/                # exploratory notebooks
├─ experiments/              # small pointers to runs (not checked in large files)
├─ models/                   # small models (large models ignored or LFS)
└─ scripts/                  # convenience scripts (start, eval, viz)
```

## Setup

### Environment Variables (.env)

You can configure runtime options using a `.env` file in the project root. Copy `.env.example` to `.env` and adjust as needed:

```
cp .env.example .env
```

- `RENDER=1` — Enable Pygame rendering during agent training/evaluation (shows a game window)
- `RENDER=0` — Run headless (no GUI window, default)

The training scripts will automatically use this variable to control rendering. You can also override it on the command line:

```
RENDER=1 python -m src.flappy.app.train_agent
```


### Requirements

**Python 3.10 is required for full compatibility with Pygame, especially for font rendering.**
Newer Python versions (e.g., 3.14) may cause errors with the `pygame.font` module due to unresolved compatibility issues.

- **Python 3.10** (do not use 3.12 or higher for flappy bird game)
- **Pygame** and other dependencies are listed in `requirements.txt`.

### macOS: Install SDL2 Libraries

Pygame requires SDL2 libraries on macOS. Install them with Homebrew:

```sh
brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf pkg-config
```

### Devcontainer or Local Setup

1. **Open in VS Code**: Use "Open in Container" or Codespaces for full devcontainer support.
2. **Dependencies**: On first start, dependencies from `requirements.txt` are installed automatically.
3. **Python Extension**: The devcontainer includes the VS Code Python extension for venv and linting support.
4. **Virtual Environment (optional)**:
    - Create: `python -m venv .venv`
    - Activate: `source .venv/bin/activate`
    - Install deps: `pip install -r requirements.txt`
5. **Run Games**:
    - Flappy Bird: `python src/flappy/app/flappy_bird.py`
    - Snake: `python src/snake/app/snake.py`

## Notes on GUI

These games open a separate window using Pygame. If running in a cloud devcontainer (e.g., Codespaces), GUI output may not be visible unless X11 forwarding or a browser-based GUI is configured. For headless training or evaluation, use the Gym environment scripts, which do not require a display.

## Running and Training Agents (Gym Environments)

### Project Structure for Agents and Training

- All runnable scripts (manual play, gym runners, training) are in `src/flappy/app/` and `src/snake/app/`.
- Gym environment wrappers are in `src/flappy/env/` and `src/snake/env/`.
- Core game logic is in `src/flappy/game.py` and `src/snake/game.py`.
- Agent implementations go in `src/flappy/agents/` and `src/snake/agents/`.

### Running a Random Agent (Headless)

- Flappy Bird: `python -m src.flappy.app.train_agent`
- Snake:    `python -m src.snake.app.train_agent` (if implemented)

This will run the agent in the Gym environment and print episode results to the terminal. You can add new agents to the `agents/` folder and update the training script to use them.

### Writing Your Own Agent

- Implement your agent as a class in the `agents/` folder (see `random_agent.py` for an example).
- Update or create a training script in `app/` to use your agent.

**Tip:** Always use the `-m` flag from the project root to run scripts that import from `src/` (e.g., `python -m src.flappy.app.train_agent`).

## Contributing

Pull requests and issues are welcome!
