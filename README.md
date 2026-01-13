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

## Setup (in Devcontainer)

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

These games open a separate window using Pygame. If running in a cloud devcontainer (e.g., Codespaces), GUI output may not be visible unless X11 forwarding or a browser-based GUI is configured.

## Contributing

Pull requests and issues are welcome!
