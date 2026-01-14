# Copilot Instructions for my-ai-games

This project is a collection of AI-powered games built with Python and Pygame. The main games are Flappy Bird and Snake, each with their own entry point scripts. The codebase is structured for experimentation and extension, with a focus on simplicity and clarity for rapid prototyping.

## Architecture Overview
- **Games are organized by folder** under `src/` (e.g., `flappy/`, `snake/`).
- **Each game has an `app/` directory** containing the main script to run the game (e.g., `flappy_bird.py`, `snake.py`).
- **Common utilities, environments, and training code** are referenced in the README but may not be present in all folders. If missing, assume the project is in a minimal state.
- **No deep service boundaries**—each game script is self-contained, handling its own game loop, rendering, and input.

## Developer Workflows
- **Run games directly:**
  - Flappy Bird: `python src/flappy/app/flappy_bird.py`
  - Snake: `python src/snake/app/snake.py`
- **Python 3.10 is required** for full compatibility, especially with Pygame font rendering. Avoid Python 3.12+.
- **Install dependencies:** `pip install -r requirements.txt`
- **On macOS, install SDL2 libraries:**
  - `brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf pkg-config`
- **Restart games from within the UI:**
  - Flappy Bird: Press SPACE after game over
  - Snake: Press R after game over

## Project-Specific Patterns
- **Game logic and rendering are tightly coupled** in each main script. There is no separation between model, view, and controller.
- **Pygame is the only external dependency** (see `requirements.txt`).
- **Scores and game state are managed in local variables**; no persistence or external communication.
- **Input handling is event-driven** via Pygame's event loop.
- **No test or build scripts** are present; manual execution is the norm.
- **Minimal configuration:** Most parameters (screen size, speeds, colors) are hardcoded in the main scripts.

## Integration Points
- **No external APIs or model integrations** are present in the current codebase.
- **If adding AI agents or training code, follow the folder conventions** described in the README (e.g., use `src/snake/train/` for RL scripts).

## Key Files & Directories
- `src/flappy/app/flappy_bird.py`: Flappy Bird game loop and logic
- `src/snake/app/snake.py`: Snake game loop and logic
- `requirements.txt`: Python dependencies (Pygame)
- `pyproject.toml`: Python version constraints
- `README.md`: Setup, architecture, and workflow notes

## Example: Adding a New Game
- Create a new folder under `src/` (e.g., `src/tetris/`).
- Add an `app/` directory with a main script (e.g., `tetris.py`).
- Follow the pattern of self-contained game logic and event-driven input.

---

If any conventions or patterns are unclear, please ask for clarification or provide feedback to improve these instructions.
