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
# "Plassy" logosundaki orman/gece temasına uyarlanmış palet
COLOR_BG = (16, 36, 22)              # koyu orman yeşili (gece zemini)
COLOR_GRID = (22, 48, 28)
COLOR_TOPBAR = (14, 30, 18)
COLOR_TEXT = (232, 240, 220)
COLOR_TEXT_DIM = (150, 185, 150)
COLOR_ACCENT = (140, 214, 110)       # logo'daki açık pastel yeşil
COLOR_ACCENT_DARK = (70, 140, 65)

COLOR_SNAKE_HEAD = (140, 214, 110)
COLOR_SNAKE_BODY = (96, 178, 88)
COLOR_SNAKE_OUTLINE = (18, 40, 22)

COLOR_FOOD = (214, 84, 78)
COLOR_FOOD_OUTLINE = (150, 44, 44)

COLOR_SPECIAL_FOOD = (242, 196, 70)   # logo'daki altın/sarı desen rengi
COLOR_SPECIAL_FOOD_OUTLINE = (176, 122, 30)

COLOR_WALL = (90, 90, 100)

COLOR_BUTTON = (24, 52, 30)
COLOR_BUTTON_HOVER = (34, 68, 40)
COLOR_BUTTON_BORDER = (140, 214, 110)

COLOR_GAMEOVER_OVERLAY = (0, 0, 0, 160)  # alpha'lı overlay

# ---- Dosya Yolları ----
HIGH_SCORE_FILE = "highscores.json"
FONT_NAME = None  # None -> pygame varsayılan fontu kullanır

# ---- Pixel-Art Sprite Ayarları ----
USE_SPRITES = True             # False yapılırsa eski vektörel çizim kullanılır (yedek mod)
SPRITE_DIR = "assets/sprites"
SPRITE_SOURCE_SIZE = 128       # generate_sprites.py çıktısının piksel boyutu (128x128 PNG)

# ---- Oyun Ayarları ----
STARTING_LENGTH = 3
SPECIAL_FOOD_CHANCE = 0.15      # Her yem üretiminde özel yem çıkma ihtimali
SPECIAL_FOOD_DURATION = 5.0     # Özel yemin ekranda kalma süresi (saniye)
SPECIAL_FOOD_SCORE = 5
NORMAL_FOOD_SCORE = 1

WRAP_AROUND = False  # True olursa yılan duvardan geçip diğer taraftan çıkar
