import pygame
import os

class CutsceneDescida:
    def __init__(self, screen, largura, altura, assets_path):
        self.screen = screen
        self.W = largura
        self.H = altura

        # Carregar imagens da cutscene
        self.frames = [
            pygame.image.load(os.path.join(assets_path, "descida_1.png")).convert_alpha(),
            pygame.image.load(os.path.join(assets_path, "descida_2.png")).convert_alpha(),
            pygame.image.load(os.path.join(assets_path, "descida_3.png")).convert_alpha(),
            pygame.image.load(os.path.join(assets_path, "descida_4.png")).convert_alpha()
        ]

        # Redimensionar todas
        self.frames = [
            pygame.transform.smoothscale(img, (self.W, self.H)) for img in self.frames
        ]

        self.index = 0            # qual imagem está aparecendo
        self.fade = 255           # fade-in das imagens
        self.fade_speed = 4
        self.wait_time = 90      # frames para esperar antes do fade-out
        self.wait_counter = 0
        self.state = "fade_in"    # fade_in → hold → fade_out → próximo frame

    def update(self):
        # FASE 1 — Fade-in
        if self.state == "fade_in":
            self.fade -= self.fade_speed
            if self.fade <= 0:
                self.fade = 0
                self.state = "hold"

        # FASE 2 — Pausa na imagem
        elif self.state == "hold":
            self.wait_counter += 1
            if self.wait_counter >= self.wait_time:
                self.state = "fade_out"

        # FASE 3 — Fade-out
        elif self.state == "fade_out":
            self.fade += self.fade_speed
            if self.fade >= 255:
                self.fade = 255
                self.wait_counter = 0
                self.index += 1

                if self.index >= len(self.frames):
                    return "end_cutscene"

                self.state = "fade_in"

    def draw(self):
        self.screen.blit(self.frames[self.index], (0, 0))

        # desenhar fade
        if self.fade > 0:
            fade_surf = pygame.Surface((self.W, self.H))
            fade_surf.fill((0,0,0))
            fade_surf.set_alpha(self.fade * 0.6)
            self.screen.blit(fade_surf, (0,0))

    def click(self):
        # Se clicar, avança imediatamente
        self.state = "fade_out"
        self.fade = 0
