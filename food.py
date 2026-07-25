import random
import time
import pygame
from settings import (
    CELL_SIZE,
    GRID_WIDTH,
    GRID_HEIGHT,
    TOPBAR_HEIGHT,
    SPECIAL_FOOD_CHANCE,
    SPECIAL_FOOD_DURATION,
    COLOR_FOOD,
    COLOR_FOOD_OUTLINE,
    COLOR_SPECIAL_FOOD,
    COLOR_SPECIAL_FOOD_OUTLINE,
)


class Food:
    def __init__(self):
        self.position = (0, 0)
        self.is_special = False
        self.spawn_time = 0
        self._pulse_phase = 0.0

    def respawn(self, occupied_cells):
        free_cells = [
            (x, y)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
            if (x, y) not in occupied_cells
        ]

        if not free_cells:
            self.position = occupied_cells[0]
            return

        self.position = random.choice(free_cells)
        self.is_special = random.random() < SPECIAL_FOOD_CHANCE
        self.spawn_time = time.time()

    def is_expired(self):
        if not self.is_special:
            return False
        return (time.time() - self.spawn_time) > SPECIAL_FOOD_DURATION

    def remaining_ratio(self):
        if not self.is_special:
            return 1.0

        elapsed = time.time() - self.spawn_time
        return max(0.0, 1.0 - (elapsed / SPECIAL_FOOD_DURATION))

    def draw(self, surface, sprites=None):
        gx, gy = self.position

        rect = pygame.Rect(
            gx * CELL_SIZE,
            gy * CELL_SIZE + TOPBAR_HEIGHT,
            CELL_SIZE,
            CELL_SIZE,
        )

        if sprites is not None and sprites.available:
            img = sprites.food_special if self.is_special else sprites.food_apple
            surface.blit(img, rect.topleft)

            if self.is_special:
                self._draw_timer_ring(surface, rect)

            return

        if self.is_special:
            color = COLOR_SPECIAL_FOOD
            outline = COLOR_SPECIAL_FOOD_OUTLINE

            ratio = self.remaining_ratio()
            center = rect.center
            radius = CELL_SIZE // 2 - 2

            pygame.draw.circle(surface, color, center, radius)
            pygame.draw.circle(surface, outline, center, radius, width=2)

            if ratio > 0:
                end_angle = -90 + 360 * ratio

                pygame.draw.arc(
                    surface,
                    (255, 255, 255),
                    rect.inflate(4, 4),
                    _deg_to_rad(-90),
                    _deg_to_rad(end_angle),
                    2,
                )

        else:
            color = COLOR_FOOD
            outline = COLOR_FOOD_OUTLINE

            inner_rect = rect.inflate(-6, -6)

            pygame.draw.circle(
                surface,
                color,
                inner_rect.center,
                inner_rect.width // 2,
            )

            pygame.draw.circle(
                surface,
                outline,
                inner_rect.center,
                inner_rect.width // 2,
                width=2,
            )

    def _draw_timer_ring(self, surface, rect):
        ratio = self.remaining_ratio()

        if ratio <= 0:
            return

        end_angle = -90 + 360 * ratio

        pygame.draw.arc(
            surface,
            (255, 255, 255),
            rect.inflate(4, 4),
            _deg_to_rad(-90),
            _deg_to_rad(end_angle),
            2,
        )


def _deg_to_rad(deg):
    import math
    return math.radians(deg)