# 🐍 PlaPy: Pixel-Art Snake Game

A fully featured, pixel-art themed Snake game built with Python and Pygame.

PlaPy combines classic Snake gameplay with custom pixel-art graphics, multiple difficulty levels, persistent high scores, bonus food mechanics, sound effects, and a polished menu system.

---

## ✨ Features

- 🎨 Custom pixel-art sprites
- 🌲 Forest/night themed visuals
- 🎮 Main menu with difficulty selection
- ⚡ Three difficulty levels (Easy, Medium, Hard)
- ⏸ Pause and resume functionality
- 💀 Game over screen with replay options
- 🏆 Persistent high score system
- 🍎 Normal and bonus food mechanics
- 🔊 Procedurally generated sound effects (no external audio files required)
- 🖱 Keyboard and mouse support
- 🛡 Automatic fallback rendering if sprite assets are missing
- 🔄 Optional screen wrap-around mode

---

## 📋 Requirements

Before running the game, make sure you have:

- Python 3.8 or higher
- Pygame
- Pillow (PIL)

All required Python packages are listed in `requirements.txt`.

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/twnar/PlaPy.git
cd PlaPy
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Game

From the project root directory, run:

```bash
python main.py
```

---

## 🎮 Controls

| Key | Action |
|-------|----------|
| Arrow Keys / WASD | Move the snake |
| P | Pause / Resume |
| ESC | Pause / Resume |
| Enter | Start game / Replay after game over |
| Mouse | Navigate menus and click buttons |

---

## 📁 Project Structure

```text
PlaPy/
├── main.py                  # Main game loop and state management
├── snake.py                 # Snake logic, movement, collisions, rendering
├── food.py                  # Normal and bonus food system
├── settings.py              # Configuration, colors, difficulty settings
├── ui.py                    # Buttons, menus, HUD rendering
├── highscore.py             # High score saving/loading
├── sounds.py                # Runtime-generated sound effects
├── assets.py                # Sprite loading and scaling
├── generate_sprites.py      # Pixel-art sprite generator
├── assets/
│   └── sprites/
│       ├── head_up.png
│       ├── head_down.png
│       ├── head_left.png
│       ├── head_right.png
│       ├── body_straight.png
│       ├── body_turn.png
│       ├── tail.png
│       ├── food_apple.png
│       ├── food_special.png
│       ├── grass_0.png
│       └── grass_1.png
├── highscores.json
├── requirements.txt
└── README.md
```

---

## 🎨 Regenerating Pixel-Art Sprites

The repository already includes all generated sprite files, so no additional setup is required.

If you'd like to customize the artwork, colors, or sprite shapes:

```bash
python generate_sprites.py
```

The script will recreate all sprite PNG files inside:

```text
assets/sprites/
```

---

## ⚙️ Configuration

Several gameplay options can be adjusted inside `settings.py`.

### Disable Pixel-Art Sprites

```python
USE_SPRITES = False
```

Switches rendering to the built-in vector renderer.

### Enable Screen Wrap-Around

```python
WRAP_AROUND = True
```

Allows the snake to pass through one edge of the screen and reappear on the opposite side.

---

## 📝 Notes

- High scores are stored separately for each difficulty level.
- High scores are saved in `highscores.json`.
- If no audio device is available, the game automatically switches to silent mode.
- If sprite files are missing or corrupted, the game automatically falls back to vector rendering instead of crashing.
- The game can be played entirely with either keyboard or mouse navigation.

---

## 🛠 Built With

- Python
- Pygame
- Pillow (PIL)

---

## 📄 License

This project is open-source and available under the MIT License.