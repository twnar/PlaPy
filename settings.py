"""
settings.py
Oyun genelinde kullanılan sabitler, renkler ve ayarlar burada tanımlanır.
"""

# ---- Ekran Ayarları ----
CELL_SIZE = 24            # Her bir hücrenin piksel boyutu
GRID_WIDTH = 25           # Yatayda kaç hücre var
GRID_HEIGHT = 20          # Dikeyde kaç hücre var

SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT + 60   # Üst bilgi çubuğu için +60 piksel
TOPBAR_HEIGHT = 60

FPS = 60  # Oyunun render FPS'i (yılanın hızı ayrı bir zamanlayıcı ile kontrol edilir)

# ---- Zorluk Seviyeleri (yılanın saniyede kaç hücre ilerlediği) ----
DIFFICULTY_LEVELS = {
    "Kolay": 8,
    "Orta": 12,
    "Zor": 18,
}

# ---- Renkler (R, G, B) ----
COLOR_BG = (18, 20, 24)
COLOR_GRID = (28, 31, 38)
COLOR_TOPBAR = (24, 26, 32)
COLOR_TEXT = (235, 235, 235)
COLOR_TEXT_DIM = (150, 150, 155)
COLOR_ACCENT = (80, 220, 120)
COLOR_ACCENT_DARK = (40, 160, 90)

COLOR_SNAKE_HEAD = (90, 230, 130)
COLOR_SNAKE_BODY = (60, 190, 110)
COLOR_SNAKE_OUTLINE = (20, 60, 35)

COLOR_FOOD = (235, 90, 90)
COLOR_FOOD_OUTLINE = (140, 30, 30)

COLOR_SPECIAL_FOOD = (245, 200, 60)
COLOR_SPECIAL_FOOD_OUTLINE = (150, 110, 10)

COLOR_WALL = (90, 90, 100)

COLOR_BUTTON = (40, 44, 52)
COLOR_BUTTON_HOVER = (55, 60, 70)
COLOR_BUTTON_BORDER = (80, 220, 120)

COLOR_GAMEOVER_OVERLAY = (0, 0, 0, 160)  # alpha'lı overlay

# ---- Dosya Yolları ----
HIGH_SCORE_FILE = "highscores.json"
FONT_NAME = None  # None -> pygame varsayılan fontu kullanır

# ---- Oyun Ayarları ----
STARTING_LENGTH = 3
SPECIAL_FOOD_CHANCE = 0.15      # Her yem üretiminde özel yem çıkma ihtimali
SPECIAL_FOOD_DURATION = 5.0     # Özel yemin ekranda kalma süresi (saniye)
SPECIAL_FOOD_SCORE = 5
NORMAL_FOOD_SCORE = 1

WRAP_AROUND = False  # True olursa yılan duvardan geçip diğer taraftan çıkar
