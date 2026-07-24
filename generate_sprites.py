"""
generate_sprites.py
Logo görselindeki yılan temasına uygun pixel-art sprite'lar üretir.
Her sprite küçük bir "pixel grid" (örn. 16x16 veya 24x24) üzerinde
elle tanımlanan renk haritalarıyla çizilir, sonra nearest-neighbor
ile büyütülüp PNG olarak kaydedilir. Böylece net, keskin pixel-art
görünümü elde edilir (bulanıklık yok).

Palet, gönderilen "Plassy" logosundaki renklere dayanır:
- Koyu orman yeşili tonları (arka plan / gölgeler)
- Açık pastel yeşil (yılan gövdesi)
- Sarı / altın (yılan desenleri, özel yem)
- Kahverengi (ağaç gövdeleri, opsiyonel dekor)
- Krem/beyaz (göz, highlight)
"""

from PIL import Image
import os

OUT_DIR = "assets/sprites"
os.makedirs(OUT_DIR, exist_ok=True)

SCALE = 8  # her "pixel" kaç ekran pikseline büyüsün

# ---- Logo'dan alınan renk paleti ----
TRANSPARENT = (0, 0, 0, 0)
OUTLINE = (18, 40, 22, 255)          # kalın siyah-yeşil kontur
BODY_LIGHT = (140, 214, 110, 255)     # açık pastel yeşil (gövde üst)
BODY_MID = (96, 178, 88, 255)         # orta yeşil (gövde gölge)
BODY_DARK = (58, 130, 62, 255)        # koyu yeşil (gövde alt gölge)
BELLY = (200, 232, 150, 255)          # karın rengi (açık sarı-yeşil)
PATTERN_GOLD = (232, 188, 74, 255)    # desen: altın/sarı oval
PATTERN_GOLD_DARK = (186, 138, 40, 255)
EYE_WHITE = (250, 248, 235, 255)
EYE_BLACK = (20, 18, 16, 255)
TONGUE = (198, 60, 70, 255)

GRASS_DARK = (26, 58, 34, 255)
GRASS_MID = (34, 74, 42, 255)
GRASS_LIGHT = (44, 92, 52, 255)

FRUIT_RED = (214, 84, 78, 255)
FRUIT_RED_DARK = (150, 44, 44, 255)
FRUIT_HL = (250, 190, 170, 255)
LEAF_GREEN = (96, 178, 88, 255)

SPECIAL_GOLD = (242, 196, 70, 255)
SPECIAL_GOLD_DARK = (176, 122, 30, 255)
SPECIAL_HL = (255, 240, 190, 255)


def make_grid(w, h, fill=TRANSPARENT):
    return [[fill for _ in range(w)] for _ in range(h)]


def save_grid(grid, name):
    h = len(grid)
    w = len(grid[0])
    img = Image.new("RGBA", (w, h), TRANSPARENT)
    px = img.load()
    for y in range(h):
        for x in range(w):
            px[x, y] = grid[y][x]
    img = img.resize((w * SCALE, h * SCALE), Image.NEAREST)
    path = os.path.join(OUT_DIR, name)
    img.save(path)
    print("Saved:", path, img.size)


def outline_and_fill(grid, cells, color, outline=True):
    """cells: set of (x,y) tuples to fill with color."""
    for (x, y) in cells:
        grid[y][x] = color
    if outline:
        h = len(grid)
        w = len(grid[0])
        for (x, y) in cells:
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in cells:
                    if grid[ny][nx] == TRANSPARENT:
                        grid[ny][nx] = OUTLINE


# =====================================================================
# YILAN BAŞI (4 yön: up, down, left, right) - 16x16 grid
# =====================================================================
def build_head(direction):
    N = 16
    grid = make_grid(N, N)

    # Kafa gövdesi, düz gövde parçasıyla AYNI dikey banda (y=2..13) oturtulur
    # ki segmentler arasında kesiksiz, hizalı bir görünüm olsun.
    body_cells = set()
    for y in range(2, 14):
        for x in range(1, 15):
            body_cells.add((x, y))
    # sadece burun tarafındaki (sağ) köşeleri hafifçe yuvarla
    corners_cut = [(14, 2), (14, 3), (14, 12), (14, 13)]
    for c in corners_cut:
        body_cells.discard(c)

    outline_and_fill(grid, body_cells, BODY_LIGHT)

    # Gölge (alt yarı biraz daha koyu)
    shadow_cells = {(x, y) for (x, y) in body_cells if y >= 9}
    for (x, y) in shadow_cells:
        grid[y][x] = BODY_MID

    # Desen (altın oval leke - kafanın üstünde)
    pattern_cells = {(5, 4), (6, 4), (7, 4), (5, 5), (8, 5)}
    for (x, y) in pattern_cells:
        if (x, y) in body_cells:
            grid[y][x] = PATTERN_GOLD

    # Gözler (sağa bakan pozisyon baz alınır)
    for (x, y) in [(9, 5), (10, 5), (9, 6), (10, 6)]:
        grid[y][x] = EYE_WHITE
    grid[6][10] = EYE_BLACK
    grid[5][10] = EYE_BLACK
    # göz konturu
    for (x, y) in [(8, 4), (8, 5), (8, 6), (8, 7), (11, 4), (11, 5), (11, 6), (11, 7),
                   (9, 4), (10, 4), (9, 7), (10, 7)]:
        if grid[y][x] == TRANSPARENT:
            grid[y][x] = OUTLINE

    # Dil (küçük kırmızı çatal - burnun ucunda)
    grid[7][15] = TONGUE
    grid[8][15] = TONGUE

    # Yöne göre döndür
    rotations = {"right": 0, "down": 1, "left": 2, "up": 3}
    k = rotations[direction]
    for _ in range(k):
        grid = rotate90(grid)

    return grid


def rotate90(grid):
    """90 derece saat yönünde döndürür (kare grid varsayımıyla)."""
    n = len(grid)
    new_grid = make_grid(n, n)
    for y in range(n):
        for x in range(n):
            new_grid[x][n - 1 - y] = grid[y][x]
    return new_grid


# =====================================================================
# YILAN GÖVDE PARÇASI (düz, yatay) - 16x16
# =====================================================================
def build_body_straight():
    N = 16
    grid = make_grid(N, N)
    cells = {(x, y) for x in range(0, 16) for y in range(2, 14)}
    outline_and_fill(grid, cells, BODY_LIGHT, outline=False)

    # üst kısım açık, alt gölgeli (silindirik hacim hissi)
    for (x, y) in cells:
        if y >= 8:
            grid[y][x] = BODY_MID
        if y >= 11:
            grid[y][x] = BODY_DARK

    # yan konturlar (üst ve alt kenar)
    for x in range(16):
        grid[2][x] = OUTLINE
        grid[13][x] = OUTLINE

    # desen: birkaç altın oval leke (sırtta, düzenli aralıklarla)
    for (x, y) in [(2, 4), (3, 4), (2, 5), (7, 5), (8, 5), (8, 6), (12, 4), (13, 4), (12, 5)]:
        grid[y][x] = PATTERN_GOLD
    for (x, y) in [(3, 5), (9, 6), (13, 5)]:
        grid[y][x] = PATTERN_GOLD_DARK

    return grid


# =====================================================================
# YILAN KIVRIM PARÇASI (köşe - sağdan aşağıya döner gibi) - 16x16
# =====================================================================
def build_body_turn():
    """Soldan girip aşağıya çıkan L-şekilli kıvrım parçası (16x16)."""
    N = 16
    grid = make_grid(N, N)
    cells = set()
    # Yatay kol: sol kenardan merkeze (y=2..13 aralığında, x=0..13)
    for x in range(0, 14):
        for y in range(2, 14):
            cells.add((x, y))
    # Dikey kol: merkezden alt kenara (x=2..13 aralığında, y=2..16)
    for x in range(2, 14):
        for y in range(2, 16):
            cells.add((x, y))

    outline_and_fill(grid, cells, BODY_LIGHT, outline=True)

    # Gölge: dış kavis (sol-alt bölge)
    for (x, y) in list(cells):
        if x <= 6 and y >= 9:
            grid[y][x] = BODY_MID
        if y >= 12:
            grid[y][x] = BODY_DARK

    # desen
    for (x, y) in [(3, 4), (4, 4), (3, 5)]:
        if (x, y) in cells:
            grid[y][x] = PATTERN_GOLD
    for (x, y) in [(8, 9), (9, 10), (8, 10)]:
        if (x, y) in cells:
            grid[y][x] = PATTERN_GOLD

    return grid


# =====================================================================
# YILAN KUYRUĞU (sivrilen uç, sağa bakan) - 16x16
# =====================================================================
def build_tail():
    """Soldan (gövde genişliğinde) başlayıp sağda sivrilen kuyruk (16x16)."""
    N = 16
    grid = make_grid(N, N)
    cells = set()
    start_top, start_bottom = 2, 14  # gövdeyle aynı genişlikte başla
    for x in range(0, 15):
        taper = int((x / 14) * 5.5)  # 0 -> 0, 14 -> ~5.5
        top = start_top + taper
        bottom = start_bottom - taper
        if top < bottom:
            for y in range(top, bottom):
                cells.add((x, y))

    outline_and_fill(grid, cells, BODY_MID)
    for (x, y) in list(cells):
        if y >= 8:
            grid[y][x] = BODY_DARK
    for (x, y) in [(2, 5), (3, 5)]:
        if (x, y) in cells:
            grid[y][x] = PATTERN_GOLD
    return grid


# =====================================================================
# NORMAL YEM: küçük pixel-art elma
# =====================================================================
def build_apple():
    N = 16
    grid = make_grid(N, N)
    body_cells = set()
    for y in range(6, 14):
        for x in range(3, 13):
            body_cells.add((x, y))
    for c in [(3, 6), (3, 7), (12, 6), (12, 7), (3, 13), (12, 13)]:
        body_cells.discard(c)

    outline_and_fill(grid, body_cells, FRUIT_RED)
    for (x, y) in body_cells:
        if x >= 9:
            grid[y][x] = FRUIT_RED_DARK

    # highlight
    for (x, y) in [(5, 8), (6, 8), (5, 9)]:
        grid[y][x] = FRUIT_HL

    # sap ve yaprak
    grid[4][8] = (110, 70, 40, 255)
    grid[5][8] = (110, 70, 40, 255)
    for (x, y) in [(9, 4), (10, 4), (10, 5), (9, 5)]:
        grid[y][x] = LEAF_GREEN
    for (x, y) in [(8, 4), (11, 5)]:
        grid[y][x] = OUTLINE

    return grid


# =====================================================================
# ÖZEL YEM: parlayan altın yıldız/gem
# =====================================================================
def build_special_food():
    N = 16
    grid = make_grid(N, N)
    # elmas şeklinde
    diamond = set()
    cx, cy = 8, 8
    for y in range(3, 13):
        for x in range(3, 13):
            if abs(x - cx) + abs(y - cy) <= 6:
                diamond.add((x, y))
    outline_and_fill(grid, diamond, SPECIAL_GOLD)
    for (x, y) in diamond:
        if (x - cx) + (y - cy) > 2:
            grid[y][x] = SPECIAL_GOLD_DARK
    for (x, y) in [(6, 6), (7, 6), (6, 7)]:
        grid[y][x] = SPECIAL_HL
    return grid


# =====================================================================
# ARKA PLAN ÇİM KAROSU (2 varyant - satranç tahtası deseni için)
# =====================================================================
def build_grass_tile(variant):
    N = 16
    base = GRASS_MID if variant == 0 else GRASS_DARK
    grid = make_grid(N, N, fill=base)
    import random
    random.seed(variant * 7 + 3)

    # ince çim yaprakları (küçük dikey çizgiler)
    blade_color = GRASS_LIGHT if variant == 0 else GRASS_MID
    for _ in range(6):
        x = random.randint(1, 14)
        y0 = random.randint(6, 12)
        length = random.randint(2, 4)
        for i in range(length):
            yy = y0 - i
            if 0 <= yy < N:
                grid[yy][x] = blade_color

    # rastgele küçük doku noktaları
    dot_color = GRASS_DARK if variant == 0 else (18, 44, 24, 255)
    for _ in range(8):
        x = random.randint(0, 15)
        y = random.randint(0, 15)
        grid[y][x] = dot_color

    # nadiren küçük bir "ışık" (ateş böceği izlenimi)
    if variant == 1 and random.random() < 0.5:
        fx, fy = random.randint(3, 12), random.randint(3, 12)
        grid[fy][fx] = (245, 220, 120, 255)

    return grid


# =====================================================================
# ÜRETİM
# =====================================================================
if __name__ == "__main__":
    for d in ["right", "left", "up", "down"]:
        save_grid(build_head(d), f"head_{d}.png")

    save_grid(build_body_straight(), "body_straight.png")
    save_grid(build_body_turn(), "body_turn.png")
    save_grid(build_tail(), "tail.png")
    save_grid(build_apple(), "food_apple.png")
    save_grid(build_special_food(), "food_special.png")
    save_grid(build_grass_tile(0), "grass_0.png")
    save_grid(build_grass_tile(1), "grass_1.png")

    print("Tüm sprite'lar üretildi.")
