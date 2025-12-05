# screens/ending.py
import pygame
from ui.utils import wrap_text

class EndingScreen:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.W = screen.get_width()
        self.H = screen.get_height()

        self.text = (
            "Ao acessar o console final do bunker, vocês descobrem os últimos registros da antiga civilização humana.\n\n"
            "Os arquivos confirmam: o foguete foi usado para evacuar um grupo seleto de pessoas para um planeta distante, "
            "codinome Nibiru. Após o lançamento, todos os sinais de comunicação cessaram.\n\n"
            "Nenhum retorno. Nenhuma confirmação. Apenas coordenadas, silêncio… e o rastro de uma sociedade que "
            "abandonou seu próprio mundo.\n\n"
            "Para Cout, Garden e Gevet, não é apenas um mistério histórico. É um grande enigma desse planeta.\n\n"
            "Este é o fim de Silent Earth.\n"
            "Pelo menos eles aprenderam sobre um conceito não conhecido antigamente por eles." \
            "Cybersegurança."
        )

        self.lines = wrap_text(self.text, self.font, int(self.W * 0.8))

    def update(self):
        pass

    def draw(self):
        self.screen.fill((0, 0, 0))

        title = self.font.render("FIM", True, (200, 220, 255))
        self.screen.blit(title, (self.W//2 - title.get_width()//2, int(self.H * 0.12)))

        y = int(self.H * 0.25)
        for line in self.lines:
            surf = self.font.render(line, True, (230, 230, 230))
            self.screen.blit(surf, (self.W//2 - surf.get_width()//2, y))
            y += surf.get_height() + 5

        info = self.font.render("Clique para voltar ao menu", True, (180, 180, 180))
        self.screen.blit(info, (self.W//2 - info.get_width()//2, int(self.H * 0.9)))

    def click(self):
        return "menu"
