import pygame
from ui.dialogue_manager import DialogueManager

class DialogueScreen:
    def __init__(self, screen, font, dialogue_path, asset_path, filename):
        self.screen = screen

        # ORDEM CORRETA:
        # screen, font, asset_path, dialogue_path
        self.manager = DialogueManager(screen, font, asset_path, dialogue_path)

        self.manager.load_dialogue(filename)

    def update(self):
        self.manager.update()

    def draw(self):
        self.manager.draw()

    def click(self):
        return self.manager.click()
