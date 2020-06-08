import contextlib
with contextlib.redirect_stdout(None):
    import pygame as pg
pg.init()

DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 960
ENV = 'dev'
