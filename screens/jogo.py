# screens/jogo.py
from ui.utils import fade, draw_text_button

def screen_jogo(state, screen, click_once):
    w,h = screen.get_width(), screen.get_height()
    font = state["font"]

    screen.fill((0,0,20))
    t = font.render("Início do Jogo - Parte 1: A descoberta do computador do FBI...", True, (255,255,255))
    screen.blit(t, (w//2 - t.get_width()//2, h//2))

    if draw_text_button(screen, "MENU", w*0.05, h*0.05, w*0.12, h*0.07, click_once, font):
        state["current"] = "menu"
        state["fade"] = 255

    state["fade"] = fade(screen, w, h, state["fade"])
