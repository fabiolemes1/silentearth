import pygame

class IntroStory:
    def __init__(self, screen, font, largura, altura):
        self.screen = screen
        self.font = font
        self.L = largura
        self.H = altura

        self.text_lines = [
            "Ano: 2850",
            "",
            "Após séculos viajando pelo universo,",
            "indivíduos do planeta Vask seguem vagando",
            "em busca de qualquer sinal de vida existente.",
            "",
            "Até que no dia de hoje se deparam com algo...",
            "",
            "Uma anomalia energética desconhecida surge nos sensores,",
            "indicando a possível existência de um planeta habitável —",
            "ou de algo que um dia já foi."
        ]

        # Fade de entrada
        self.fade_alpha = 255
        self.fade_speed = 3

        # Fade de saída
        self.exiting = False
        self.exit_alpha = 0


    def update(self):
        # Fade-in
        if not self.exiting and self.fade_alpha > 0:
            self.fade_alpha -= self.fade_speed
            if self.fade_alpha < 0:
                self.fade_alpha = 0

        # Fade-out ao clicar
        if self.exiting:
            self.exit_alpha += 10
            if self.exit_alpha >= 255:
                return "go_to_cutscene"


    def draw(self):
        self.screen.fill((0, 0, 0))

        # Calcular altura total para centralizar
        total_text_height = sum(self.font.size(line)[1] + 10 for line in self.text_lines)
        start_y = self.H / 2 - total_text_height / 2

        y = start_y
        for line in self.text_lines:
            txt = self.font.render(line, True, (255, 255, 255))
            x = self.L / 2 - txt.get_width() / 2
            self.screen.blit(txt, (x, y))
            y += txt.get_height() + 10

        # Mostrar instrução
        info = self.font.render("Clique para continuar...", True, (180, 180, 180))
        self.screen.blit(info, (self.L/2 - info.get_width()/2, self.H*0.85))

        # Fade-in
        if self.fade_alpha > 0:
            fade = pygame.Surface((self.L, self.H))
            fade.fill((0,0,0))
            fade.set_alpha(self.fade_alpha)
            self.screen.blit(fade, (0,0))

        # Fade-out
        if self.exiting:
            fade = pygame.Surface((self.L, self.H))
            fade.fill((0,0,0))
            fade.set_alpha(self.exit_alpha)
            self.screen.blit(fade, (0,0))


    def click(self):
        self.exiting = True
