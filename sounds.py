import numpy as np
import pygame


class SoundManager:
    def __init__(self):
        self.enabled = True
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2)
            self.eat_sound = self._make_tone(440, 0.08, volume=0.25)
            self.special_sound = self._make_tone(880, 0.12, volume=0.25)
            self.gameover_sound = self._make_tone(160, 0.35, volume=0.3, fade=True)
            self.click_sound = self._make_tone(600, 0.05, volume=0.15)
        except Exception:
            self.enabled = False

    def _make_tone(self, frequency, duration, volume=0.3, fade=False):
        sample_rate = 44100
        n_samples = int(sample_rate * duration)
        t = np.linspace(0, duration, n_samples, False)
        wave = np.sin(frequency * t * 2 * np.pi)

        if fade:
            fade_curve = np.linspace(1, 0, n_samples)
            wave = wave * fade_curve

        mono = (wave * volume * 32767).astype(np.int16)
        stereo = np.column_stack((mono, mono))
        return pygame.sndarray.make_sound(np.ascontiguousarray(stereo))

    def play_eat(self):
        if self.enabled:
            self.eat_sound.play()

    def play_special(self):
        if self.enabled:
            self.special_sound.play()

    def play_gameover(self):
        if self.enabled:
            self.gameover_sound.play()

    def play_click(self):
        if self.enabled:
            self.click_sound.play()

