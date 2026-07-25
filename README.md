# 🐍 Snake Game — Python & Pygame

A fully featured, multi-file **pixel-art themed** Snake game.

The visual style is inspired by the forest/night aesthetic and pixel-art snake character from the "Plassy" logo.

## Features

- **Pixel-art graphics**: Custom-made sprites for the snake head (4 directions), body, turns, tail, apple, special food, and forest ground tiles
- **Main menu**: Difficulty selection (Easy / Medium / Hard)
- **3 difficulty levels**: Snake speed changes based on the selected difficulty
- **Pause menu**: Pause the game with `P` or `ESC`
- **Game over screen**: Displays the score and provides Play Again / Main Menu options
- **High score system**: Persistent difficulty-based records stored in `highscores.json`
- **Normal + Special (Bonus) Food**: Special food disappears after a short time, grants more points, and grows the snake by 2 segments
- **Sound effects**: Real-time generated sounds without requiring external audio files (eating, collision, button clicks)
- **Mouse-supported interface**: Menus can be controlled with both keyboard and mouse
- **Automatic fallback mode**: If sprite PNG files are missing, the game falls back to the vector-based renderer instead of crashing

## Installation

```bash
pip install -r requirements.txt
```

## Running the Game

```bash
python main.py
```

## Controls

| Key | Function |
|------|----------|
| Arrow Keys / WASD | Move the snake |
| P / ESC | Pause / Resume |
| Enter | Start from menu, play again after game over |
| Mouse | Click menu buttons |

## Project Structure

```text
snake_game/
├── main.py                  # Game loop and state machine (menu/game/pause/game over)
├── snake.py                 # Snake class: movement, growth, collisions, sprite/vector rendering
├── food.py                  # Normal and special (bonus) food logic
├── settings.py              # Constants, colors (forest theme), difficulty settings
├── ui.py                    # Button component and HUD (score bar) rendering
├── highscore.py             # JSON-based high score saving/loading
├── sounds.py                # Real-time generated sound effects using pygame
├── assets.py                # Loads and scales pixel-art sprites
├── generate_sprites.py      # Script that generates sprite PNG files using Pillow
├── assets/
│   └── sprites/             # Generated pixel-art PNG files
│       ├── head_up.png, head_down.png, head_left.png, head_right.png
│       ├── body_straight.png, body_turn.png, tail.png
│       ├── food_apple.png, food_special.png
│       └── grass_0.png, grass_1.png
├── requirements.txt
└── README.md
```

## Regenerating Pixel-Art Sprites

The sprites are included as ready-to-use PNG files in the `assets/sprites/` directory, so you can run the game immediately.

If you want to modify the color palette or sprite shapes, edit `generate_sprites.py` and run:

```bash
python generate_sprites.py
```

This script uses Pillow (PIL) and recreates all PNG files inside the `assets/sprites/` directory.

## Notes

- High scores are stored separately for each difficulty level in `highscores.json`.
- If no audio device is available (for example, on some servers), the game automatically switches to silent mode without errors.
- If the `assets/sprites/` directory is missing or corrupted, the game automatically falls back to the vector rendering mode, even if `USE_SPRITES = True` is enabled in `settings.py`.
- Setting `USE_SPRITES = False` in `settings.py` will disable pixel-art graphics and use the vector renderer instead.
- Setting `WRAP_AROUND = True` in `settings.py` allows the snake to pass through walls and reappear on the opposite side.