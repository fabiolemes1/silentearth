import pygame

class IntroScene:
    def __init__(self, screen, largura, altura, assets_path):
        self.screen = screen
        self.L = largura
        self.H = altura

        # Carrega a imagem da nave com os três personagens
        self.bg = pygame.image.load(
            assets_path + "/juntos_nave.png"
        ).convert_alpha()

        # redimensiona
        self.bg = pygame.transform.smoothscale(self.bg, (self.L, self.H))

        # Fade-in inicial
        self.fade = 255
        self.fade_speed = 1

        # Para fade-out quando clicar
        self.exiting = False
        self.exit_alpha = 0

    def update(self):
        # Fade-in
        if not self.exiting and self.fade > 0:
            self.fade -= self.fade_speed
            if self.fade < 0:
                self.fade = 0

        # Fade-out
        if self.exiting:
            self.exit_alpha += 12
            if self.exit_alpha >= 255:
                return "go_to_dialogue"

    def draw(self):
        self.screen.blit(self.bg, (0,0))

        # “Clique para continuar”
        font = pygame.font.SysFont("consolas", 30)
        txt = font.render("Clique para continuar...", True, (255,255,255))
        self.screen.blit(txt, (self.L/2 - txt.get_width()/2, self.H*0.9))

        # Fade-in
        if self.fade > 0:
            fade = pygame.Surface((self.L, self.H))
            fade.fill((0,0,0))
            fade.set_alpha(self.fade)
            self.screen.blit(fade, (0,0))

        # Fade-out
        if self.exiting:
            fade = pygame.Surface((self.L, self.H))
            fade.fill((0,0,0))
            fade.set_alpha(self.exit_alpha)
            self.screen.blit(fade, (0,0))

    def click(self):
        self.exiting = True
