# screens/menu.py
import pygame

from ui.button import Button
from ui.utils import fade

def screen_menu(state, screen, assets, buttons, click_once):
    w, h = screen.get_width(), screen.get_height()

    screen.blit(assets["bg"], (0,0))

    title = assets["title"]
    rect = title.get_rect(center=(w//2, int(h*0.40)))
    screen.blit(title, rect)

    # botões grandes
    for b in buttons.values():
        b.draw(screen, click_once)

    state["fade"] = fade(screen, w, h, state["fade"])
