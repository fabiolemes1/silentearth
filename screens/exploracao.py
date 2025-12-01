# screens/exploracao.py
import pygame
import os

class ExploracaoScreen:
    def __init__(self, screen, assets, state, assets_path):
        self.screen = screen
        self.assets = assets
        self.state = state
        self.assets_path = assets_path

        # Tamanho da tela
        self.W = screen.get_width()
        self.H = screen.get_height()

        # Carregar mapa
        self.bg = pygame.image.load(os.path.join(assets_path, "mapa_exploracao.png")).convert()
        self.bg = pygame.transform.smoothscale(self.bg, (self.W, self.H))

        # =========================
        # SPRITE DO COMPUTADOR
        # =========================
        self.computador_img = pygame.image.load(
            os.path.join(assets_path, "computador.png")
        ).convert_alpha()

        # Escala (50% do tamanho original)
        scale = 0.80
        self.computador_img = pygame.transform.smoothscale(
            self.computador_img,
            (int(self.computador_img.get_width()*scale),
             int(self.computador_img.get_height()*scale))
        )

        self.computador_rect = self.computador_img.get_rect(
            center=(int(self.W * 0.60), int(self.H * 0.60))
        )

        # =========================
        # SPRITES DOS DOCUMENTOS
        # =========================
        self.doc_imgs = []
        self.doc_rects = []

        doc_names = ["documento1.png", "documento2.png", "documento3.png"]

        positions = [
        (0.32, 0.78),   # Documento 1
        (0.45, 0.82),   # Documento 2
        (0.67, 0.82),   # Documento 3
]

        for name, (xf, yf) in zip(doc_names, positions):
            img = pygame.image.load(os.path.join(assets_path, name)).convert_alpha()

            # Escalar para 30%
            img = pygame.transform.smoothscale(
                img,
                (int(img.get_width() * 0.15), int(img.get_height() * 0.15))
            )

            rect = img.get_rect(center=(int(self.W*xf), int(self.H*yf)))

            self.doc_imgs.append(img)
            self.doc_rects.append(rect)

        # Documentos começam travados (não clicáveis)
        self.docs_liberados = False

        # Beep misterioso
        self.beep = pygame.mixer.Sound(os.path.join(assets_path, "sinal_beep.mp3"))
        self.beep.set_volume(0.6)
        self.beep.play(-1)

        # Hover
        self.hover_computador = False
        self.hover_docs = [False, False, False]

    # =========================
    def update(self):
        mx, my = pygame.mouse.get_pos()

        # Hover no computador
        self.hover_computador = self.computador_rect.collidepoint((mx, my))

        # Hover nos documentos (só se liberados)
        self.hover_docs = []
        for rect in self.doc_rects:
            self.hover_docs.append(rect.collidepoint((mx, my)) if self.docs_liberados else False)

    # =========================
    def draw(self):
        # Fundo
        self.screen.blit(self.bg, (0, 0))

        # Computador
        self.screen.blit(self.computador_img, self.computador_rect)

        if self.hover_computador:
            glow = pygame.Surface((self.computador_rect.width, self.computador_rect.height), pygame.SRCALPHA)
            glow.fill((255,255,255,60))
            self.screen.blit(glow, self.computador_rect.topleft)

        # Documentos
        for img, rect, hover in zip(self.doc_imgs, self.doc_rects, self.hover_docs):
            self.screen.blit(img, rect)
            if hover:
                glow = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
                glow.fill((255,255,255,50))
                self.screen.blit(glow, rect.topleft)

    # =========================
    def click(self):
        mx, my = pygame.mouse.get_pos()

        # Clique no computador
        if self.computador_rect.collidepoint((mx, my)):
            self.beep.stop()
            if self.docs_liberados:
                return "abrir_minigame_senha"
            return "abrir_dialogo_computador"

        # Clique nos documentos (somente depois do diálogo)
        if self.docs_liberados:
            for i, rect in enumerate(self.doc_rects):
                if rect.collidepoint((mx, my)):
                    return f"abrir_documento_{i+1}"

        return None

    # =========================
    # Chamado quando o diálogo do computador acaba
    # =========================
    def liberar_documentos(self):
        self.docs_liberados = True
