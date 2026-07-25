import pygame
from settings import (
    CELL_SIZE,
    GRID_WIDTH,
    GRID_HEIGHT,
    TOPBAR_HEIGHT,
    STARTING_LENGTH,
    WRAP_AROUND,
    COLOR_SNAKE_HEAD,
    COLOR_SNAKE_BODY,
    COLOR_SNAKE_OUTLINE,
)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        cx, cy = GRID_WIDTH // 2, GRID_HEIGHT // 2
        self.body = [(cx - i, cy) for i in range(STARTING_LENGTH)]
        self.direction = RIGHT
        self.pending_direction = RIGHT
        self.grow_pending = 0
        self.alive = True

    def set_direction(self, new_direction):
        opposite = (-self.direction[0], -self.direction[1])

        if new_direction == opposite:
            return

        self.pending_direction = new_direction

    def grow(self, amount=1):
        self.grow_pending += amount

    def move(self):
        self.direction = self.pending_direction

        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        if WRAP_AROUND:
            new_head = (
                new_head[0] % GRID_WIDTH,
                new_head[1] % GRID_HEIGHT,
            )
        else:
            if (
                not (0 <= new_head[0] < GRID_WIDTH)
                or not (0 <= new_head[1] < GRID_HEIGHT)
            ):
                self.alive = False
                return

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

    def draw(self, surface, sprites=None):
        if sprites is not None and sprites.available:
            self._draw_sprites(surface, sprites)
        else:
            self._draw_vector(surface)

    @staticmethod
    def _dir_name(vec):
        return {
            UP: "up",
            DOWN: "down",
            LEFT: "left",
            RIGHT: "right",
        }[vec]

    def _draw_sprites(self, surface, sprites):
        n = len(self.body)

        for i, (gx, gy) in enumerate(self.body):
            px = gx * CELL_SIZE
            py = gy * CELL_SIZE + TOPBAR_HEIGHT

            if i == 0:
                img = sprites.head[self._dir_name(self.direction)]

            elif i == n - 1:
                vec = (
                    self.body[i - 1][0] - gx,
                    self.body[i - 1][1] - gy,
                )

                tail_dir = (
                    self._dir_name((-vec[0], -vec[1]))
                    if vec in (UP, DOWN, LEFT, RIGHT)
                    else "right"
                )

                img = sprites.tail_rotated(tail_dir)

            else:
                prev_seg = self.body[i - 1]
                next_seg = self.body[i + 1]

                img = self._body_sprite(
                    sprites,
                    prev_seg,
                    (gx, gy),
                    next_seg,
                )

            surface.blit(img, (px, py))

    def _body_sprite(self, sprites, prev_seg, cur, next_seg):
        gx, gy = cur

        in_vec = (
            gx - prev_seg[0],
            gy - prev_seg[1],
        )

        out_vec = (
            next_seg[0] - gx,
            next_seg[1] - gy,
        )

        if in_vec == out_vec:
            vertical = in_vec in (UP, DOWN)
            return sprites.body_straight(vertical=vertical)

        pairs_to_angle = {
            (RIGHT, DOWN): 0,
            (UP, LEFT): 0,
            (DOWN, LEFT): 90,
            (RIGHT, UP): 90,
            (LEFT, UP): 180,
            (DOWN, RIGHT): 180,
            (UP, RIGHT): 270,
            (LEFT, DOWN): 270,
        }

        angle = pairs_to_angle.get((in_vec, out_vec), 0)

        return sprites.body_turn_rotated(angle)

    def _draw_vector(self, surface):
        for i, (gx, gy) in enumerate(self.body):
            rect = pygame.Rect(
                gx * CELL_SIZE,
                gy * CELL_SIZE + TOPBAR_HEIGHT,
                CELL_SIZE,
                CELL_SIZE,
            )

            color = (
                COLOR_SNAKE_HEAD
                if i == 0
                else COLOR_SNAKE_BODY
            )

            inner_rect = rect.inflate(-3, -3)

            pygame.draw.rect(
                surface,
                color,
                inner_rect,
                border_radius=6,
            )

            pygame.draw.rect(
                surface,
                COLOR_SNAKE_OUTLINE,
                inner_rect,
                width=2,
                border_radius=6,
            )

            if i == 0:
                self._draw_eyes(surface, rect)

    def _draw_eyes(self, surface, rect):
        dx, dy = self.direction
        eye_radius = 2
        offset = CELL_SIZE // 4

        cx, cy = rect.center

        perp = (-dy, dx)

        eye1 = (
            cx + dx * offset + perp[0] * offset,
            cy + dy * offset + perp[1] * offset,
        )

        eye2 = (
            cx + dx * offset - perp[0] * offset,
            cy + dy * offset - perp[1] * offset,
        )

        pygame.draw.circle(
            surface,
            (10, 10, 10),
            (int(eye1[0]), int(eye1[1])),
            eye_radius,
        )

        pygame.draw.circle(
            surface,
            (10, 10, 10),
            (int(eye2[0]), int(eye2[1])),
            eye_radius,
        )