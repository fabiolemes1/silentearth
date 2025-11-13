# screens/opcoes.py
import pygame
from ui.utils import fade, draw_slider, draw_text_button

def screen_opcoes(state, screen, assets, click_once):
    w, h = screen.get_width(), screen.get_height()

    screen.fill((25,25,35))

    font = state["font"]
    t = font.render("Opções de Áudio", True, (255,255,255))
    screen.blit(t, (w//2 - t.get_width()//2, int(h*0.12)))

    # Volume label + ícone
    barra_x = w*0.35
    barra_y = h*0.45
    barra_w = w*0.3
    barra_h = int(h*0.01)

    # Ícone volume
    icon = assets["volume"]
    screen.blit(icon, (barra_x - w*0.07, barra_y - icon.get_height()//2))

    # Texto "Música"
    lab = font.render("Música", True, (255,255,255))
    screen.blit(lab, (barra_x - w*0.11 - lab.get_width(), barra_y - lab.get_height()//2))

    # Slider
    state["volume"] = draw_slider(screen, barra_x, barra_y, barra_w, barra_h, state["volume"], click_once)
    if not state["muted"]:
        pygame.mixer.music.set_volume(state["volume"])

    # Botão mute
    ic = assets["unmute"] if state["muted"] else assets["mute"]
    ic_rect = ic.get_rect(center=(int(w*0.5), int(h*0.6)))
    screen.blit(ic, ic_rect)

    if click_once and ic_rect.collidepoint(pygame.mouse.get_pos()):
        state["muted"] = not state["muted"]
        pygame.mixer.music.set_volume(0.0 if state["muted"] else state["volume"])

    # Botão voltar
    if draw_text_button(screen, "VOLTAR", w*0.4, h*0.82, w*0.2, h*0.08, click_once, font):
        state["current"] = "menu"
        state["fade"] = 255

    state["fade"] = fade(screen, w, h, state["fade"])
