# ui/button.py
import pygame
import numpy as np

class Button:
    def __init__(self, image, x_frac, y_frac, screen_w, screen_h, action=None):
        self.image = image
        self.action = action
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.x_frac = x_frac
        self.y_frac = y_frac

        self.update_rect()

    def update_rect(self):
        self.rect = self.image.get_rect(
            center=(int(self.screen_w * self.x_frac),
                    int(self.screen_h * self.y_frac))
        )

    def draw(self, screen, click_once):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            hover = self._brighten()
            screen.blit(hover, self.rect)
            if click_once and self.action:
                self.action()
        else:
            screen.blit(self.image, self.rect)

    def _brighten(self):
        s = self.image.copy()
        arr = pygame.surfarray.pixels3d(s)
        arr[:] = np.clip(arr * 1.25, 0, 255)
        del arr
        return s