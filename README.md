# 🐍 Snake Game

A classic Snake game built with Python and [Pygame](https://www.pygame.org/).

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Pygame](https://img.shields.io/badge/pygame-2.5%2B-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

## Features

- Smooth grid-based movement (arrow keys or WASD)
- Score tracking with a running "best score"
- Snake speeds up gradually as it grows
- Pause / resume support
- Game-over screen with quick restart
- No external assets — pure code, runs anywhere Pygame runs

## Demo

```
Score: 120                                   Best: 150

  .  .  .  .  .  .  .  .  .  .  .  .  .  .
  .  .  .  ███████▓▓▓  .  .  .  .  .  .  .
  .  .  .  .  .  .  .  .  .  ●  .  .  .  .
  .  .  .  .  .  .  .  .  .  .  .  .  .  .
```

## Requirements

- Python 3.8+
- Pygame 2.5+

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/snake-game.git
cd snake-game

# 2. (Optional but recommended) create a virtual environment
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python snake_game.py
```

### Controls

| Key                 | Action          |
|----------------------|----------------|
| Arrow keys / WASD     | Move the snake |
| `P`                   | Pause / unpause |
| `R`                   | Restart after game over |
| `Esc`                 | Quit |

## How It Works

The game runs on a fixed grid. The snake is represented as a list of `(x, y)`
coordinates, with the head at index `0`. Each tick:

1. The next head position is computed from the current direction.
2. Wall and self-collisions end the game.
3. If the new head lands on the food, the snake grows and a new food tile spawns; otherwise the tail is trimmed to keep the length constant.
4. Speed increases slightly every few food items eaten, up to a cap.

All game logic lives in `snake_game.py` inside the `SnakeGame` class — feel free to tweak constants like `CELL_SIZE`, `FPS_START`, or colors at the top of the file to customize it.

## Possible Improvements

Contributions and forks welcome! Some ideas:

- [ ] Add sound effects
- [ ] Add obstacles / walls per level
- [ ] Add a main menu screen
- [ ] Persist high score to a file
- [ ] Add a "wrap around edges" mode

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.
