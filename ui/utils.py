# ui/utils.py
import pygame

def fade(screen, width, height, alpha):
    if alpha > 0:
        overlay = pygame.Surface((width, height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(alpha)
        screen.blit(overlay, (0, 0))
    return max(0, alpha - 12)

def draw_text_button(screen, text, x, y, w, h, click_once, font, base_color=(100,100,100)):
    rect = pygame.Rect(int(x), int(y), int(w), int(h))
    mx, my = pygame.mouse.get_pos()
    color = base_color
    clicked = False

    if rect.collidepoint((mx,my)):
        color = (150,150,150)
        if click_once:
            clicked = True

    pygame.draw.rect(screen, color, rect, border_radius=10)
    pygame.draw.rect(screen, (0,180,255), rect, 3, border_radius=10)

    txt = font.render(text, True, (255,255,255))
    screen.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))

    return clicked

def draw_slider(screen, x, y, w, h, value, click_once):
    bar_rect = pygame.Rect(x, y-h//2, w, h)
    pygame.draw.rect(screen, (255,255,255), bar_rect, 2)

    pos_x = int(x + value * w)
    pygame.draw.circle(screen, (0,180,255), (pos_x, y), max(8, int(h*2)))

    mx, my = pygame.mouse.get_pos()
    pressed = pygame.mouse.get_pressed()[0]

    new_value = value

    if pressed and bar_rect.inflate(0,40).collidepoint((mx,my)):
        new_value = (mx - x) / w

    if click_once and bar_rect.collidepoint((mx,my)):
        new_value = (mx - x) / w

    return max(0, min(1, new_value))

def wrap_text(text, font, max_width):
    words = text.split(" ")
    lines = []
    current = ""

    for word in words:
        test = current + word + " "
        if font.size(test)[0] <= max_width:
            current = test
        else:
            lines.append(current)
            current = word + " "
    lines.append(current)
    return lines
