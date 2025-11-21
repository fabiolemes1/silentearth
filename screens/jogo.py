from screens.minigame_password import MinigamePassword
from ui.utils import fade

def screen_jogo(state, screen, click_once, events):
    w, h = screen.get_width(), screen.get_height()
    
    # Initialize minigame if not present
    if "minigame" not in state:
        state["minigame"] = MinigamePassword(state)

    # Update and Draw Minigame
    minigame = state["minigame"]
    minigame.handle_input(events)
    minigame.draw(screen)

    # Fade effect (optional, keeping it if desired, but usually terminal is crisp)
    # state["fade"] = fade(screen, w, h, state["fade"])
