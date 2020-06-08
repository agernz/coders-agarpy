import math
import random as rand
from player import Player
from blob import Blob
from world import World
from utils import process_input
from constants import pg, DISPLAY_WIDTH, DISPLAY_HEIGHT, ENV


def draw_sprites(sprites):
    for sprite in sprites:
        sprite.draw(DISPLAY)


pg.display.set_caption('AgarPy')
DISPLAY = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
BACKGROUND = pg.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
BACKGROUND.fill((0, 0, 0))
CLOCK = pg.time.Clock()

DELTA_T = 30
MAX_FRAME_TIME = 250
running = True
acc = 0
fps_timer = 0

world = World()
DISPLAY.blit(BACKGROUND, (0, 0))
world.draw(draw_sprites)

while running:
    running = process_input(world.players[0])

    delta_time = CLOCK.tick()
    if delta_time > MAX_FRAME_TIME:
        print("ERROR")
    acc += min(delta_time, MAX_FRAME_TIME)
    while acc >= DELTA_T:
        if ENV == 'dev':
            fps_timer += 1
            # update every half second
            if fps_timer == 15:
                pg.display.set_caption(str(CLOCK.get_fps()))
                fps_timer = 0
        world.update()
        acc -= DELTA_T
    world.interpolate(float(acc) / DELTA_T)

    DISPLAY.blit(BACKGROUND, (0, 0))
    world.draw(draw_sprites)
    pg.display.update()

pg.quit()
