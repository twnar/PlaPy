# PlaPy

A Snake game with a hand-built pixel-art forest theme, written in Python with Pygame. Three difficulty levels, per-difficulty high scores, bonus food, procedurally generated sound (no audio files to ship), and a full menu/pause/game-over flow.

## Features

- Pixel-art sprites (head/body/tail/food/grass tiles) in a forest/night palette
- Main menu with Easy / Medium / Hard difficulty select
- Pause and resume, mid-run
- Game over screen with a one-key replay
- High scores saved per difficulty in `highscores.json`
- Normal and bonus food, bonus food on a timer
- All sound effects generated at runtime — no `.wav`/`.mp3` assets
- Keyboard (arrows/WASD) or mouse-driven menus
- Falls back to a vector renderer automatically if sprite files are missing or fail to load
- Optional screen wrap-around instead of wall collision

## Requirements

- Python 3.8+
- Pygame
- Pillow

## Install

```bash
git clone https://github.com/twnar/PlaPy.git
cd PlaPy
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Controls

| Input | Action |
|---|---|
| Arrow keys / WASD | Move |
| P / Esc | Pause / resume |
| Enter | Start / replay |
| Mouse | Menu navigation |

## Project layout

```
PlaPy/
├── main.py                # game loop, state machine
├── snake.py                # movement, collision, rendering
├── food.py                 # normal + bonus food spawning
├── settings.py             # colors, tuning, difficulty presets
├── ui.py                   # menus, HUD, buttons
├── highscore.py            # load/save highscores.json
├── sounds.py               # runtime-synthesized SFX
├── assets.py               # sprite loading/scaling
├── generate_sprites.py     # sprite generator (see below)
├── assets/sprites/         # head_*, body_*, tail, food_*, grass_*
├── highscores.json
└── requirements.txt
```

## Regenerating sprites

Sprites are already committed, so this is only needed if you want to tweak the art:

```bash
python generate_sprites.py
```

This overwrites everything in `assets/sprites/`.

## Configuration

Edit `settings.py`:

```python
USE_SPRITES = False   # use the vector renderer instead of pixel-art sprites
WRAP_AROUND = True    # snake wraps around screen edges instead of dying on walls
```

## Notes

- High scores are tracked independently per difficulty.
- No audio device detected → game runs silently, no crash.
- Missing/corrupt sprite files → falls back to vector rendering, no crash.

## Built with

Python · Pygame · Pillow

## License

MIT — see `LICENSE`.
