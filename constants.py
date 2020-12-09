import contextlib
with contextlib.redirect_stdout(None):
    import pygame as pg
pg.init()

DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 320
