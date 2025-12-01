import pygame
import json
import os

from ui.utils import wrap_text


class DialogueManager:
    def __init__(self, screen, font, asset_path, dialogue_path):
        self.screen = screen
        self.font = font
        self.asset_path = asset_path
        self.dialogue_path = dialogue_path

        self.W = screen.get_width()
        self.H = screen.get_height()

        self.dialogue = []
        self.index = 0

        # Efeito de digitação
        self.text_speed = 3
        self.timer = 0
        self.char_index = 0

        self.wrapped_lines = []


    # ===============================================================
    def load_dialogue(self, filename):
        path = os.path.join(self.dialogue_path, filename)

        if not os.path.exists(path):
            raise FileNotFoundError(f"Dialogue file not found: {path}")

        with open(path, "r", encoding="utf-8") as f:
            self.dialogue = json.load(f)

        self.index = 0
        self._load_entry()


    # ===============================================================
    def _load_entry(self):
        self.current = self.dialogue[self.index]
        self.text = self.current.get("text", "")

        # Reset typing
        self.char_index = 0
        self.timer = 0

        # Quebra de linha do texto COMPLETO
        self.wrapped_lines = wrap_text(self.text, self.font, int(self.W * 0.85))


    # ===============================================================
    def update(self):
        if self.char_index < len(self.text):
            self.timer += 1
            if self.timer >= self.text_speed:
                self.timer = 0
                self.char_index += 1


    # ===============================================================
    def click(self):
        # Completar texto imediatamente
        if self.char_index < len(self.text):
            self.char_index = len(self.text)
            return None

        # Obter ação se houver
        action = self.current.get("action", None)
        nxt = self.current.get("next", None)

        # Fim
        if nxt == "END":
            return "END"

        # Se for índice
        if isinstance(nxt, int):
            self.index = nxt
            self._load_entry()
            return action

        # Se não tiver next, vai para o próximo
        if nxt is None:
            if self.index + 1 < len(self.dialogue):
                self.index += 1
                self._load_entry()
                return action
            return action

        # Se for string (nome do personagem ou outro marcador)
        if isinstance(nxt, str):
            for i, entry in enumerate(self.dialogue):
                if entry.get("speaker") == nxt:
                    self.index = i
                    self._load_entry()
                    return action

        return action


    # ===============================================================
    def draw_background(self):
        entry = self.dialogue[self.index]
        bg = entry.get("bg", None)

        if bg:
            try:
                img = pygame.image.load(os.path.join(self.asset_path, bg)).convert()
                img = pygame.transform.scale(img, (self.W, self.H))
                self.screen.blit(img, (0, 0))
            except:
                self.screen.fill((0, 0, 0))
        else:
            self.screen.fill((0, 0, 0))


    # ===============================================================
    def draw_textbox(self):
        box_y = int(self.H * 0.72)
        box_height = int(self.H * 0.28)

        # CAIXA SEMI-TRANSPARENTE
        textbox = pygame.Surface((self.W, box_height), pygame.SRCALPHA)
        textbox.fill((0, 0, 0, 140))   # <-- AQUI define a transparência
        self.screen.blit(textbox, (0, box_y))

        entry = self.dialogue[self.index]
        speaker = entry.get("speaker", "")

        # Nome do personagem
        if speaker and speaker != "CUTSCENE":
            name_surface = self.font.render(speaker, True, (255, 255, 100))
            self.screen.blit(name_surface, (40, box_y + 20))

        # Texto com quebra de linha
        display_text = self.text[:self.char_index]
        wrapped = wrap_text(display_text, self.font, int(self.W * 0.85))

        y = box_y + 60
        for line in wrapped:
            line_surf = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(line_surf, (40, y))
            y += line_surf.get_height() + 4


    # ===============================================================
    def draw(self):
        self.draw_background()
        self.draw_textbox()
