# main.py
import pygame
import sys
import os

from config.display import create_screen, FULLSCREEN

from screens.menu import screen_menu
from screens.opcoes import screen_opcoes
from screens.creditos import screen_creditos
from screens.jogo import screen_jogo

from screens.dialogue_intro import DialogueIntro
from screens.intro_story import IntroStory
from screens.intro_scene import IntroScene
from screens.exploracao import ExploracaoScreen
from screens.cutscene_descida import CutsceneDescida

from screens.dialogue import DialogueScreen
from ui.button import Button

pygame.init()
pygame.mixer.init()


# =====================================================================
# CONFIGURAÇÃO BÁSICA DA TELA
# =====================================================================
screen, LARGURA, ALTURA = create_screen(FULLSCREEN)

FONT = pygame.font.SysFont("consolas", max(18, int(ALTURA * 0.035)))

ASSETS_PATH = os.path.join(os.getcwd(), "assets")
DIALOGUE_PATH = os.path.join(os.getcwd(), "data", "dialogues")


# =====================================================================
# FUNÇÃO PARA CARREGAR IMAGENS
# =====================================================================
def load_and_scale(name, scale=None):
    img = pygame.image.load(os.path.join(ASSETS_PATH, name)).convert_alpha()
    if scale:
        img = pygame.transform.smoothscale(img, scale)
    return img


# =====================================================================
# CARREGAR TODOS OS ASSETS
# =====================================================================
def load_assets():
    assets = {}

    # fundo menu
    assets["bg"] = load_and_scale("silent_earth_interface.png", (LARGURA, ALTURA))

    # título
    base_title = pygame.image.load(os.path.join(ASSETS_PATH, "silent_earth_titulo.png")).convert_alpha()
    tw = int(base_title.get_width() * 2.2)
    th = int(base_title.get_height() * 2.2)
    assets["title"] = pygame.transform.smoothscale(base_title, (tw, th))

    # botões
    btn_scale = int(LARGURA * 0.28)

    def scale_button(name):
        base = pygame.image.load(os.path.join(ASSETS_PATH, name)).convert_alpha()
        prop = base.get_height() / base.get_width()
        return pygame.transform.smoothscale(base, (btn_scale, int(btn_scale * prop)))

    assets["btn_jogar"] = scale_button("botao_jogar.png")
    assets["btn_opcoes"] = scale_button("botao_opcoes.png")
    assets["btn_creditos"] = scale_button("botao_creditos.png")

    # ícones do volume
    assets["volume"] = load_and_scale("icon_volume.png", (50, 50))
    assets["mute"] = load_and_scale("icon_mute.png", (50, 50))
    assets["unmute"] = load_and_scale("icon_unmute.png", (50, 50))

    # cutscene foguete (descida)
    # já será controlada pela CutsceneDescida
    return assets


assets = load_assets()


# =====================================================================
# INSTÂNCIAS INICIAIS
# =====================================================================
dialogue_intro = DialogueIntro(screen, FONT, ASSETS_PATH, DIALOGUE_PATH)
intro_story = IntroStory(screen, FONT, LARGURA, ALTURA)
intro_scene = IntroScene(screen, LARGURA, ALTURA, ASSETS_PATH)
cutscene_descida = CutsceneDescida(screen, LARGURA, ALTURA, ASSETS_PATH)

exploracao = None
exploracao_dialogo = None
exploracao_computador = None


# =====================================================================
# BOTÕES DO MENU
# =====================================================================
def create_menu_buttons():
    return {
        "jogar": Button(assets["btn_jogar"], 0.5, 0.55, LARGURA, ALTURA,
                        lambda: set_state("intro_story")),
        "opcoes": Button(assets["btn_opcoes"], 0.5, 0.69, LARGURA, ALTURA,
                         lambda: set_state("opcoes")),
        "creditos": Button(assets["btn_creditos"], 0.5, 0.83, LARGURA, ALTURA,
                           lambda: set_state("creditos"))
    }


buttons = create_menu_buttons()


# =====================================================================
# MÚSICA DO MENU
# =====================================================================
try:
    pygame.mixer.music.load(os.path.join(ASSETS_PATH, "silent_earth_theme.mp3"))
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
except:
    print("⚠ Música não encontrada.")


# =====================================================================
# ESTADO GLOBAL
# =====================================================================
state = {
    "current": "menu",
    "fade": 255,
    "font": FONT,
    "volume": 0.5,
    "muted": False
}


def set_state(new_state):
    state["current"] = new_state
    state["fade"] = 255


# =====================================================================
# FULLSCREEN
# =====================================================================
def toggle_fullscreen():
    global screen, LARGURA, ALTURA, FONT, assets, buttons
    global dialogue_intro, intro_story, intro_scene, cutscene_descida

    FULLSCREEN = not FULLSCREEN
    screen, LARGURA, ALTURA = create_screen(FULLSCREEN)

    FONT = pygame.font.SysFont("consolas", max(18, int(ALTURA * 0.035)))
    state["font"] = FONT

    assets = load_assets()
    buttons = create_menu_buttons()

    dialogue_intro = DialogueIntro(screen, FONT, ASSETS_PATH, DIALOGUE_PATH)
    intro_story = IntroStory(screen, FONT, LARGURA, ALTURA)
    intro_scene = IntroScene(screen, LARGURA, ALTURA, ASSETS_PATH)
    cutscene_descida = CutsceneDescida(screen, LARGURA, ALTURA, ASSETS_PATH)


# =====================================================================
# LOOP PRINCIPAL
# =====================================================================
clock = pygame.time.Clock()

while True:
    click_once = False

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            click_once = True

        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_F11:
                toggle_fullscreen()
            if ev.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # =================================================================
    # ESTADOS DO JOGO
    # =================================================================

    if state["current"] == "menu":
        screen_menu(state, screen, assets, buttons, click_once)

    elif state["current"] == "intro_story":
        result = intro_story.update()
        intro_story.draw()

        if click_once:
            intro_story.click()

        if result == "go_to_cutscene":
            set_state("intro_scene")

    elif state["current"] == "intro_scene":
        result = intro_scene.update()
        intro_scene.draw()

        if click_once:
            intro_scene.click()

        if result == "go_to_dialogue":
            set_state("intro")

    elif state["current"] == "intro":
        dialogue_intro.update()
        dialogue_intro.draw()

        if click_once:
            action = dialogue_intro.click()
            if action == "start_landing":
                set_state("cutscene_descida")

    elif state["current"] == "cutscene_descida":
        result = cutscene_descida.update()

        # SE A CUTSCENE ACABOU, NÃO CHAMA draw()
        if result == "end_cutscene":
            set_state("exploracao")
            exploracao = None
            exploracao_dialogo = None
            continue

        cutscene_descida.draw()


    elif state["current"] == "exploracao":
        if exploracao is None:
            exploracao = ExploracaoScreen(screen, assets, state, ASSETS_PATH)


        exploracao.update()
        exploracao.draw()

        if click_once:
            action = exploracao.click()
            if action == "abrir_dialogo_computador":
                exploracao_dialogo = DialogueScreen(
                    screen,
                    state["font"],
                    DIALOGUE_PATH,
                    ASSETS_PATH,
                    "exploracao_computador.json"
                )
                set_state("exploracao_dialogo")

    elif state["current"] == "exploracao_dialogo":
        exploracao_dialogo.update()
        exploracao_dialogo.draw()

        if click_once:
            action = exploracao_dialogo.click()

            if action == "END":
                exploracao.liberar_documentos()
                set_state("exploracao")


    elif state["current"] == "opcoes":
        screen_opcoes(state, screen, assets, click_once)

    elif state["current"] == "creditos":
        screen_creditos(state, screen, click_once)

    elif state["current"] == "jogo":
        screen_jogo(state, screen, click_once)

    pygame.display.flip()
    clock.tick(60)
