"""
assets.py
generate_sprites.py tarafından üretilen pixel-art PNG dosyalarını
yükler ve oyun hücre boyutuna (CELL_SIZE) göre ölçekler.
Nearest-neighbor ölçekleme kullanılır ki pixel-art netliği korunsun.
"""

import os
import pygame
from settings import CELL_SIZE, SPRITE_DIR, USE_SPRITES

_cache = {}


def _load_and_scale(filename, size=None):
    """PNG'yi yükler ve verilen boyuta (varsayılan: CELL_SIZE) nearest-neighbor ile ölçekler."""
    if size is None:
        size = (CELL_SIZE, CELL_SIZE)

    cache_key = (filename, size)
    if cache_key in _cache:
        return _cache[cache_key]

    path = os.path.join(SPRITE_DIR, filename)
    if not os.path.exists(path):
        _cache[cache_key] = None
        return None

    try:
        img = pygame.image.load(path).convert_alpha()
        # pygame.transform.scale = nearest-neighbor benzeri (smoothscale değil!)
        scaled = pygame.transform.scale(img, size)
        _cache[cache_key] = scaled
        return scaled
    except pygame.error:
        _cache[cache_key] = None
        return None


class Sprites:
    """Tüm oyun sprite'larını tek noktadan yükleyip erişime sunan sınıf."""

    def __init__(self):
        self.available = False
        if not USE_SPRITES:
            return

        cell = (CELL_SIZE, CELL_SIZE)

        self.head = {
            "up": _load_and_scale("head_up.png", cell),
            "down": _load_and_scale("head_down.png", cell),
            "left": _load_and_scale("head_left.png", cell),
            "right": _load_and_scale("head_right.png", cell),
        }
        self.body_straight_h = _load_and_scale("body_straight.png", cell)
        self.body_turn = _load_and_scale("body_turn.png", cell)
        self.tail_right = _load_and_scale("tail.png", cell)

        self.food_apple = _load_and_scale("food_apple.png", cell)
        self.food_special = _load_and_scale("food_special.png", cell)

        self.grass = [
            _load_and_scale("grass_0.png", cell),
            _load_and_scale("grass_1.png", cell),
        ]

        # Tüm temel sprite'lar başarıyla yüklendiyse pixel-art modu aktif
        self.available = all([
            self.head["up"], self.head["down"], self.head["left"], self.head["right"],
            self.body_straight_h, self.body_turn, self.tail_right,
            self.food_apple, self.food_special,
            self.grass[0], self.grass[1],
        ])

    # ---- Yardımcı döndürme fonksiyonları ----
    def body_straight(self, vertical=False):
        """Yatay düz gövde sprite'ını, gerekirse 90° döndürerek döner."""
        img = self.body_straight_h
        if vertical:
            return pygame.transform.rotate(img, 90)
        return img

    def body_turn_rotated(self, angle):
        """Kıvrım sprite'ını (varsayılan: sol->aşağı) verilen açıyla döndürür."""
        return pygame.transform.rotate(self.body_turn, angle)

    def tail_rotated(self, direction):
        """Kuyruk sprite'ını (varsayılan: sağa bakan) yöne göre döndürür."""
        angle_map = {"right": 0, "up": 90, "left": 180, "down": -90}
        return pygame.transform.rotate(self.tail_right, angle_map[direction])
