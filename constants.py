import contextlib
with contextlib.redirect_stdout(None):
    import pygame as pg
pg.init()

DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 960
ENV = 'dev'

PLAYER_COLORS = {
    'RED': (208, 0, 0),
    'YELLOW': (255, 224, 102),
    'BLUE': (36, 123, 160),
    'MINT': (112, 193, 179),
    'ORANGE': (235, 94, 40),
    'GREEN': (63, 163, 77),
    'PINK': (255, 166, 193)
}
BACKGROUND_COLOR = (255, 236, 209)
TEXT_COLOR = (0, 0, 0)
