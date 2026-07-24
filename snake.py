"""
snake.py
Yılanın kendisini temsil eden sınıf: konum, hareket, büyüme ve çizim.
"""

import pygame
from settings import (
    CELL_SIZE, GRID_WIDTH, GRID_HEIGHT, TOPBAR_HEIGHT,
    STARTING_LENGTH, WRAP_AROUND,
    COLOR_SNAKE_HEAD, COLOR_SNAKE_BODY, COLOR_SNAKE_OUTLINE,
)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        """Yılanı ekranın ortasında, başlangıç uzunluğunda yeniden oluşturur."""
        cx, cy = GRID_WIDTH // 2, GRID_HEIGHT // 2
        self.body = [(cx - i, cy) for i in range(STARTING_LENGTH)]
        self.direction = RIGHT
        self.pending_direction = RIGHT
        self.grow_pending = 0
        self.alive = True

    def set_direction(self, new_direction):
        """
        Yönü değiştirir; ancak yılanın kendi üzerine 180 derece
        dönmesine (anında geri gitmesine) izin vermez.
        """
        opposite = (-self.direction[0], -self.direction[1])
        if new_direction == opposite:
            return
        self.pending_direction = new_direction

    def grow(self, amount=1):
        """Bir sonraki hareket(ler)de kuyruğun uzamasını sağlar."""
        self.grow_pending += amount

    def move(self):
        """Yılanı bir hücre ileri taşır. Çarpışma varsa alive=False yapar."""
        self.direction = self.pending_direction
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        if WRAP_AROUND:
            new_head = (new_head[0] % GRID_WIDTH, new_head[1] % GRID_HEIGHT)
        else:
            if not (0 <= new_head[0] < GRID_WIDTH) or not (0 <= new_head[1] < GRID_HEIGHT):
                self.alive = False
                return

        # Kendi vücuduna çarpma kontrolü
        if new_head in self.body:
            self.alive = False
            return

        self.body.insert(0, new_head)
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()

    def get_head_position(self):
        return self.body[0]

    def occupies(self, pos):
        return pos in self.body

    def draw(self, surface):
        for i, (gx, gy) in enumerate(self.body):
            rect = pygame.Rect(
                gx * CELL_SIZE,
                gy * CELL_SIZE + TOPBAR_HEIGHT,
                CELL_SIZE,
                CELL_SIZE,
            )
            color = COLOR_SNAKE_HEAD if i == 0 else COLOR_SNAKE_BODY
            inner_rect = rect.inflate(-3, -3)
            pygame.draw.rect(surface, color, inner_rect, border_radius=6)
            pygame.draw.rect(surface, COLOR_SNAKE_OUTLINE, inner_rect, width=2, border_radius=6)

            # Başın üzerine küçük "gözler" çiz
            if i == 0:
                self._draw_eyes(surface, rect)

    def _draw_eyes(self, surface, rect):
        dx, dy = self.direction
        eye_radius = 2
        offset = CELL_SIZE // 4

        cx, cy = rect.center
        # Yön vektörüne göre gözlerin konumunu hafifçe kaydır
        perp = (-dy, dx)  # yöne dik vektör (iki gözü ayırmak için)

        eye1 = (cx + dx * offset + perp[0] * offset, cy + dy * offset + perp[1] * offset)
        eye2 = (cx + dx * offset - perp[0] * offset, cy + dy * offset - perp[1] * offset)

        pygame.draw.circle(surface, (10, 10, 10), (int(eye1[0]), int(eye1[1])), eye_radius)
        pygame.draw.circle(surface, (10, 10, 10), (int(eye2[0]), int(eye2[1])), eye_radius)
