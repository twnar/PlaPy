import pygame
from settings import (
    COLOR_BUTTON, COLOR_BUTTON_HOVER, COLOR_BUTTON_BORDER,
    COLOR_TEXT, COLOR_TEXT_DIM, COLOR_TOPBAR, SCREEN_WIDTH, TOPBAR_HEIGHT,
)


class Button:
    def __init__(self, rect, text, font, callback=None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.callback = callback
        self.hovered = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.callback:
                    self.callback()
                return True
        return False

    def draw(self, surface):
        color = COLOR_BUTTON_HOVER if self.hovered else COLOR_BUTTON
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, COLOR_BUTTON_BORDER, self.rect, width=2, border_radius=10)

        text_surf = self.font.render(self.text, True, COLOR_TEXT)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)


def draw_topbar(surface, font, score, high_score, difficulty):
    bar_rect = pygame.Rect(0, 0, SCREEN_WIDTH, TOPBAR_HEIGHT)
    pygame.draw.rect(surface, COLOR_TOPBAR, bar_rect)
    pygame.draw.line(surface, (50, 53, 60), (0, TOPBAR_HEIGHT), (SCREEN_WIDTH, TOPBAR_HEIGHT), 2)

    score_surf = font.render(f"Score: {score}", True, COLOR_TEXT)
    surface.blit(score_surf, (16, TOPBAR_HEIGHT // 2 - score_surf.get_height() // 2))

    high_surf = font.render(f"High Score: {high_score}", True, COLOR_TEXT_DIM)
    high_rect = high_surf.get_rect(midtop=(SCREEN_WIDTH // 2, 10))
    surface.blit(high_surf, high_rect)

    diff_surf = font.render(difficulty, True, COLOR_TEXT_DIM)
    diff_rect = diff_surf.get_rect(topright=(SCREEN_WIDTH - 16, TOPBAR_HEIGHT // 2 - diff_surf.get_height() // 2))
    surface.blit(diff_surf, diff_rect)


def draw_text_centered(surface, text, font, color, center_pos):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=center_pos)
    surface.blit(surf, rect)
    return rect