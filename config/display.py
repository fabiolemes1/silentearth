# config/display.py
import pygame
import os

pygame.init()

def get_display_settings():
    info = pygame.display.Info()
    return info.current_w, info.current_h

# resolução nativa
NATIVE_W, NATIVE_H = get_display_settings()

# fullscreen padrão
FULLSCREEN = True

def create_screen(fullscreen=True):
    if fullscreen:
        screen = pygame.display.set_mode((NATIVE_W, NATIVE_H), pygame.FULLSCREEN)
        return screen, NATIVE_W, NATIVE_H
    else:
        w = int(NATIVE_W * 0.9)
        h = int(NATIVE_H * 0.9)
        screen = pygame.display.set_mode((w, h))
        return screen, w, h
