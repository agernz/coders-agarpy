import contextlib
with contextlib.redirect_stdout(None):
    import pygame
pygame.init()

DISPLAY_WIDTH = 900
DISPLAY_HEIGHT = 900
COLORKEY = (255, 0, 255)
