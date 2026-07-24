"""
main.py
Snake oyununun giriş noktası. Durum makinesi (state machine) ile
Menü -> Oyun -> Duraklat -> Oyun Sonu ekranları arasında geçiş yapar.

Çalıştırmak için:
    pip install pygame numpy
    python main.py
"""

import sys
import pygame

from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, TOPBAR_HEIGHT, FPS,
    CELL_SIZE, GRID_WIDTH, GRID_HEIGHT,
    DIFFICULTY_LEVELS,
    COLOR_BG, COLOR_GRID, COLOR_TEXT, COLOR_TEXT_DIM, COLOR_ACCENT,
    NORMAL_FOOD_SCORE, SPECIAL_FOOD_SCORE,
)
from snake import Snake, UP, DOWN, LEFT, RIGHT
from food import Food
from ui import Button, draw_topbar, draw_text_centered
from highscore import load_high_scores, update_high_score
from sounds import SoundManager
from assets import Sprites

# ---- Durumlar ----
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_PAUSED = "paused"
STATE_GAMEOVER = "gameover"


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Yılan Oyunu - Snake")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.font_small = pygame.font.SysFont("arial", 18)
        self.font_medium = pygame.font.SysFont("arial", 26, bold=True)
        self.font_large = pygame.font.SysFont("arial", 48, bold=True)

        self.sounds = SoundManager()
        self.sprites = Sprites()
        self.high_scores = load_high_scores()

        self.state = STATE_MENU
        self.difficulty = "Orta"
        self.score = 0

        self.snake = Snake()
        self.food = Food()

        self.move_timer = 0.0
        self.new_record = False

        self.menu_buttons = self._build_menu_buttons()
        self.pause_buttons = self._build_pause_buttons()
        self.gameover_buttons = self._build_gameover_buttons()

    # ---------------------------------------------------------------
    # Buton kurulumları
    # ---------------------------------------------------------------
    def _build_menu_buttons(self):
        buttons = []
        center_x = SCREEN_WIDTH // 2
        y = 260
        for name in DIFFICULTY_LEVELS.keys():
            btn = Button(
                (center_x - 100, y, 200, 44),
                f"{name}",
                self.font_medium,
                callback=(lambda n=name: self._select_difficulty(n)),
            )
            buttons.append(btn)
            y += 56

        start_btn = Button(
            (center_x - 100, y + 10, 200, 50),
            "BAŞLA",
            self.font_medium,
            callback=self._start_game,
        )
        buttons.append(start_btn)
        return buttons

    def _build_pause_buttons(self):
        center_x = SCREEN_WIDTH // 2
        resume_btn = Button(
            (center_x - 100, 260, 200, 46),
            "Devam Et",
            self.font_medium,
            callback=self._resume_game,
        )
        menu_btn = Button(
            (center_x - 100, 320, 200, 46),
            "Ana Menü",
            self.font_medium,
            callback=self._go_to_menu,
        )
        return [resume_btn, menu_btn]

    def _build_gameover_buttons(self):
        center_x = SCREEN_WIDTH // 2
        retry_btn = Button(
            (center_x - 100, 320, 200, 46),
            "Tekrar Oyna",
            self.font_medium,
            callback=self._start_game,
        )
        menu_btn = Button(
            (center_x - 100, 380, 200, 46),
            "Ana Menü",
            self.font_medium,
            callback=self._go_to_menu,
        )
        return [retry_btn, menu_btn]

    # ---------------------------------------------------------------
    # Durum geçiş callback'leri
    # ---------------------------------------------------------------
    def _select_difficulty(self, name):
        self.difficulty = name
        self.sounds.play_click()

    def _start_game(self):
        self.sounds.play_click()
        self.snake.reset()
        self.food.respawn(self.snake.body)
        self.score = 0
        self.new_record = False
        self.move_timer = 0.0
        self.state = STATE_PLAYING

    def _resume_game(self):
        self.sounds.play_click()
        self.state = STATE_PLAYING

    def _go_to_menu(self):
        self.sounds.play_click()
        self.state = STATE_MENU

    def _pause_game(self):
        self.sounds.play_click()
        self.state = STATE_PAUSED

    # ---------------------------------------------------------------
    # Ana döngü
    # ---------------------------------------------------------------
    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            self._handle_events()
            self._update(dt)
            self._draw()
            pygame.display.flip()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                self._handle_keydown(event.key)

            if self.state == STATE_MENU:
                for btn in self.menu_buttons:
                    btn.handle_event(event)
            elif self.state == STATE_PAUSED:
                for btn in self.pause_buttons:
                    btn.handle_event(event)
            elif self.state == STATE_GAMEOVER:
                for btn in self.gameover_buttons:
                    btn.handle_event(event)

    def _handle_keydown(self, key):
        if self.state == STATE_PLAYING:
            if key in (pygame.K_UP, pygame.K_w):
                self.snake.set_direction(UP)
            elif key in (pygame.K_DOWN, pygame.K_s):
                self.snake.set_direction(DOWN)
            elif key in (pygame.K_LEFT, pygame.K_a):
                self.snake.set_direction(LEFT)
            elif key in (pygame.K_RIGHT, pygame.K_d):
                self.snake.set_direction(RIGHT)
            elif key == pygame.K_ESCAPE or key == pygame.K_p:
                self._pause_game()

        elif self.state == STATE_PAUSED:
            if key == pygame.K_ESCAPE or key == pygame.K_p:
                self._resume_game()

        elif self.state == STATE_MENU:
            if key == pygame.K_RETURN:
                self._start_game()

        elif self.state == STATE_GAMEOVER:
            if key == pygame.K_RETURN:
                self._start_game()
            elif key == pygame.K_ESCAPE:
                self._go_to_menu()

    # ---------------------------------------------------------------
    # Güncelleme mantığı
    # ---------------------------------------------------------------
    def _update(self, dt):
        if self.state != STATE_PLAYING:
            return

        speed = DIFFICULTY_LEVELS[self.difficulty]  # hücre/saniye
        step_duration = 1.0 / speed

        self.move_timer += dt
        if self.move_timer >= step_duration:
            self.move_timer -= step_duration
            self.snake.move()

            if not self.snake.alive:
                self._on_game_over()
                return

            head = self.snake.get_head_position()
            if head == self.food.position:
                if self.food.is_special:
                    self.score += SPECIAL_FOOD_SCORE
                    self.snake.grow(2)
                    self.sounds.play_special()
                else:
                    self.score += NORMAL_FOOD_SCORE
                    self.snake.grow(1)
                    self.sounds.play_eat()
                self.food.respawn(self.snake.body)

        # Özel yemin süresi dolduysa yeni yem üret
        if self.food.is_expired():
            self.food.respawn(self.snake.body)

    def _on_game_over(self):
        self.sounds.play_gameover()
        self.new_record = update_high_score(self.difficulty, self.score)
        self.high_scores = load_high_scores()
        self.state = STATE_GAMEOVER

    # ---------------------------------------------------------------
    # Çizim
    # ---------------------------------------------------------------
    def _draw(self):
        self.screen.fill(COLOR_BG)

        if self.state == STATE_MENU:
            self._draw_menu()
        elif self.state in (STATE_PLAYING, STATE_PAUSED):
            self._draw_game()
            if self.state == STATE_PAUSED:
                self._draw_pause_overlay()
        elif self.state == STATE_GAMEOVER:
            self._draw_game()
            self._draw_gameover_overlay()

    def _draw_grid(self):
        if self.sprites.available:
            for x in range(GRID_WIDTH):
                for y in range(GRID_HEIGHT):
                    variant = (x + y) % 2
                    img = self.sprites.grass[variant]
                    self.screen.blit(img, (x * CELL_SIZE, y * CELL_SIZE + TOPBAR_HEIGHT))
            return

        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                rect = pygame.Rect(
                    x * CELL_SIZE, y * CELL_SIZE + TOPBAR_HEIGHT, CELL_SIZE, CELL_SIZE
                )
                if (x + y) % 2 == 0:
                    pygame.draw.rect(self.screen, COLOR_GRID, rect)

    def _draw_game(self):
        self._draw_grid()
        self.food.draw(self.screen, self.sprites)
        self.snake.draw(self.screen, self.sprites)
        high = self.high_scores.get(self.difficulty, 0)
        draw_topbar(self.screen, self.font_small, self.score, high, self.difficulty)

    def _draw_menu(self):
        draw_text_centered(
            self.screen, "YILAN OYUNU", self.font_large, COLOR_ACCENT,
            (SCREEN_WIDTH // 2, 100)
        )
        draw_text_centered(
            self.screen, "Zorluk seç ve başla", self.font_small, COLOR_TEXT_DIM,
            (SCREEN_WIDTH // 2, 150)
        )

        # Seçili zorluğu vurgula
        for i, (name, btn) in enumerate(zip(DIFFICULTY_LEVELS.keys(), self.menu_buttons)):
            if name == self.difficulty:
                pygame.draw.rect(self.screen, COLOR_ACCENT, btn.rect, width=3, border_radius=10)

        for btn in self.menu_buttons:
            btn.draw(self.screen)

        high = self.high_scores.get(self.difficulty, 0)
        draw_text_centered(
            self.screen, f"Rekor ({self.difficulty}): {high}", self.font_small, COLOR_TEXT_DIM,
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40)
        )

        controls_text = "Yön tuşları / WASD ile hareket, P ile duraklat"
        draw_text_centered(
            self.screen, controls_text, self.font_small, COLOR_TEXT_DIM,
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20)
        )

    def _draw_pause_overlay(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        draw_text_centered(
            self.screen, "DURAKLATILDI", self.font_large, COLOR_TEXT,
            (SCREEN_WIDTH // 2, 180)
        )
        for btn in self.pause_buttons:
            btn.draw(self.screen)

    def _draw_gameover_overlay(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.screen.blit(overlay, (0, 0))

        draw_text_centered(
            self.screen, "OYUN BİTTİ", self.font_large, (235, 90, 90),
            (SCREEN_WIDTH // 2, 160)
        )
        draw_text_centered(
            self.screen, f"Skor: {self.score}", self.font_medium, COLOR_TEXT,
            (SCREEN_WIDTH // 2, 220)
        )

        if self.new_record:
            draw_text_centered(
                self.screen, "🎉 Yeni Rekor! 🎉", self.font_medium, COLOR_ACCENT,
                (SCREEN_WIDTH // 2, 260)
            )
        else:
            high = self.high_scores.get(self.difficulty, 0)
            draw_text_centered(
                self.screen, f"Rekor: {high}", self.font_medium, COLOR_TEXT_DIM,
                (SCREEN_WIDTH // 2, 260)
            )

        for btn in self.gameover_buttons:
            btn.draw(self.screen)


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
