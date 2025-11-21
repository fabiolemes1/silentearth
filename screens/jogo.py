# screens/jogo.py
import pygame
from ui.utils import fade, draw_text_button

# Estado inicial do jogador (futuro)
player_pos = [0, 0]
initialized = False

def screen_jogo(state, screen, click_once):
    global player_pos, initialized
    
    w, h = screen.get_width(), screen.get_height()
    font = state["font"]

    # Inicializa só na primeira vez
    if not initialized:
        player_pos = [w//2, h//2]
        initialized = True

    # -------------------
    # FUNDO DO MAPA
    # -------------------
    screen.fill((10, 10, 20))  # por enquanto, placeholder

    # -------------------
    # TEXTO TEMPORÁRIO
    # -------------------
    texto = "Início do Jogo - Parte 1: A descoberta do computador do FBI..."
    t = font.render(texto, True, (255,255,255))
    screen.blit(t, (w//2 - t.get_width()//2, h*0.1))

    # -------------------
    # BOTÃO MENU
    # -------------------
    if draw_text_button(screen, "MENU", w*0.04, h*0.04, w*0.13, h*0.07, click_once, font):
        state["current"] = "menu"
        state["fade"] = 255

    # -------------------
    # FADE
    # -------------------
    state["fade"] = fade(screen, w, h, state["fade"])
