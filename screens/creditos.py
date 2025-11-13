# screens/creditos.py
from ui.utils import fade, draw_text_button

def screen_creditos(state, screen, click_once):
    w,h = screen.get_width(), screen.get_height()
    font = state["font"]
    screen.fill((25,25,35))

    linhas = [
        "Silent Earth © 2025",
        "Desenvolvido por:",
        "Vinicius da Silva Araujo - 221001981",
        "Fabio Valentim Lemes da Silva - 222008584",
        "Informática e Sociedade 2025.2 - UnB"
    ]

    for i, linha in enumerate(linhas):
        t = font.render(linha, True, (255,255,255))
        screen.blit(t, (w//2 - t.get_width()//2, int(h*0.28 + i*h*0.055)))

    if draw_text_button(screen, "VOLTAR", w*0.4, h*0.82, w*0.2, h*0.08, click_once, font):
        state["current"] = "menu"
        state["fade"] = 255

    state["fade"] = fade(screen, w, h, state["fade"])
