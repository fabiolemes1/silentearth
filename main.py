# main.py
import pygame
import sys
import os

from config.display import create_screen, FULLSCREEN, NATIVE_W, NATIVE_H
from screens.menu import screen_menu
from screens.opcoes import screen_opcoes
from screens.creditos import screen_creditos
from screens.jogo import screen_jogo

pygame.init()
pygame.mixer.init()

# === TELA ==========================================================================================
screen, LARGURA, ALTURA = create_screen(FULLSCREEN)

# === FONT ==========================================================================================
FONT = pygame.font.SysFont("consolas", max(18, int(ALTURA*0.035)))

# === ASSETS PATH ====================================================================================
ASSETS_PATH = os.path.join(os.getcwd(), "assets")

# === FUNÇÃO DE CARREGA IMAGEM COM ESCALA ===========================================================
def load_and_scale(name, scale=None):
    img = pygame.image.load(os.path.join(ASSETS_PATH, name)).convert_alpha()
    if scale:
        img = pygame.transform.smoothscale(img, scale)
    return img

# === CARREGAR E ESCALAR ASSETS ======================================================================
def load_assets():
    assets = {}
    # fundo
    assets["bg"] = load_and_scale("silent_earth_interface.png", (LARGURA, ALTURA))
    # título maior (1.6x)
    title_base = pygame.image.load(os.path.join(ASSETS_PATH,"silent_earth_titulo.png")).convert_alpha()
    tw = int(title_base.get_width()*2.2)
    th = int(title_base.get_height()*2.2)
    assets["title"] = pygame.transform.smoothscale(title_base,(tw,th))

    # botões
    btn_scale = int(LARGURA*0.28)
    def scale_btn(fn):
        base = pygame.image.load(os.path.join(ASSETS_PATH,fn)).convert_alpha()
        prop = base.get_height()/base.get_width()
        return pygame.transform.smoothscale(base, (btn_scale,int(btn_scale*prop)))

    assets["btn_jogar"] = scale_btn("botao_jogar.png")
    assets["btn_opcoes"] = scale_btn("botao_opcoes.png")
    assets["btn_creditos"] = scale_btn("botao_creditos.png")

    # ícones
    ic_side = int(LARGURA*0.06)
    assets["volume"] = load_and_scale("botao_volume_desmutado.png",(ic_side,ic_side))
    assets["mute"] = load_and_scale("botao_volume_desmutado.png",(ic_side,ic_side))
    assets["unmute"] = load_and_scale("botao_volume_mutado.png",(ic_side,ic_side))

    return assets

assets = load_assets()

# === BOTÕES DO MENU (criamos depois dos assets carregados) ========================================
from ui.button import Button

def create_menu_buttons():
    return {
        "jogar": Button(assets["btn_jogar"],0.5,0.55,LARGURA,ALTURA,lambda: set_state("jogo")),
        "opcoes": Button(assets["btn_opcoes"],0.5,0.69,LARGURA,ALTURA,lambda: set_state("opcoes")),
        "creditos": Button(assets["btn_creditos"],0.5,0.83,LARGURA,ALTURA,lambda: set_state("creditos"))
    }

buttons = create_menu_buttons()

# === MÚSICA =========================================================================================
volume = 0.5
muted  = False
try:
    pygame.mixer.music.load(os.path.join(ASSETS_PATH,"silent_earth_theme.mp3"))
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)
except:
    print("⚠ Música não encontrada.")

# === ESTADO GLOBAL ====================================================================================
state = {
    "current":"menu",
    "fade":255,
    "volume":volume,
    "muted":muted,
    "font":FONT
}

def set_state(new_state):
    state["current"] = new_state
    state["fade"] = 255

# === TOGGLE FULLSCREEN ==============================================================================
def toggle_fullscreen():
    global screen,LARGURA,ALTURA,FONT,assets,buttons,FULLSCREEN

    FULLSCREEN = not FULLSCREEN

    screen, LARGURA, ALTURA = create_screen(FULLSCREEN)

    FONT = pygame.font.SysFont("consolas", max(18, int(ALTURA * 0.035)))
    state["font"] = FONT

    assets = load_assets()
    buttons = {
        "jogar": Button(assets["btn_jogar"],0.5,0.55,LARGURA,ALTURA,lambda: set_state("jogo")),
        "opcoes": Button(assets["btn_opcoes"],0.5,0.69,LARGURA,ALTURA,lambda: set_state("opcoes")),
        "creditos": Button(assets["btn_creditos"],0.5,0.83,LARGURA,ALTURA,lambda: set_state("creditos"))
    }

# === LOOP ============================================================================================
clock = pygame.time.Clock()

while True:
    click_once = False
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit(); sys.exit()

        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            click_once = True

        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_F11:
                toggle_fullscreen()
            if ev.key == pygame.K_ESCAPE:
                pygame.quit(); sys.exit()

    if state["current"] == "menu":
        screen_menu(state, screen, assets, buttons, click_once)
    elif state["current"] == "opcoes":
        screen_opcoes(state, screen, assets, click_once)
    elif state["current"] == "creditos":
        screen_creditos(state, screen, click_once)
    elif state["current"] == "jogo":
        screen_jogo(state, screen, click_once)

    pygame.display.flip()
    clock.tick(60)
