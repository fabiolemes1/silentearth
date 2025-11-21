import pygame
import os
from ui.dialogue_manager import DialogueManager

class DialogueIntro:
    def __init__(self, screen, font, asset_path, dialogue_path):
        self.screen = screen
        self.font = font
        self.asset_path = asset_path
        self.dialogue_path = dialogue_path

        # Carrega o gerenciador de diálogos
        self.manager = DialogueManager(screen, font, asset_path, dialogue_path)

        # Carrega o arquivo intro.json
        self.manager.load_dialogue("intro.json")

    def update(self):
        self.manager.update()

    def draw(self):
        self.manager.draw()

    def click(self):
        return self.manager.click()
