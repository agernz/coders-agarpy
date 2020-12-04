import math
import random as rand
from time import time, sleep
from player import Player
from blob import Blob
from world import World
from utils import process_input
from constants import pg, DISPLAY_WIDTH, DISPLAY_HEIGHT, ENV, BACKGROUND_COLOR, TEXT_COLOR


def draw_sprites(sprites):
    for sprite in sprites:
        sprite.draw(DISPLAY)


pg.display.set_caption('AgarPy')
DISPLAY = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
BACKGROUND = pg.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
BACKGROUND.fill(BACKGROUND_COLOR)
CLOCK = pg.time.Clock()

DELTA_T = 60
MAX_FRAME_TIME = 250
running = True
acc = 0
fps_timer = 0

world = World()
DISPLAY.blit(BACKGROUND, (0, 0))
world.draw(draw_sprites)

# run game for 5 minutes
timeout = time() + 300

while running:
    running = process_input(world.players[0])

    delta_time = CLOCK.tick()
    if delta_time > MAX_FRAME_TIME:
        print("ERROR - delta_ time greater than max_frame", delta_time)

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

    if time() > timeout:
        running = False

top_players = world.get_top_players()
first_font = pg.font.SysFont('chalkduster.ttf', 80)
contenders_font = pg.font.SysFont('chalkduster.ttf', 30)
fp = next(top_players)
sp = next(top_players)
tp = None
try:
    tp = next(top_players)
except:
    pass
first_text = first_font.render("{} Wins! - score: {}".format(fp.name, fp.score),
                               True, TEXT_COLOR)
second_text = contenders_font.render("2nd Place: {} - score: {}".format(sp.name, sp.score),
                                     True, TEXT_COLOR)
if tp:
    third_text = contenders_font.render("3rd Place: {} - score: {}".format(tp.name, tp.score),
                                        True, TEXT_COLOR)
text_y = DISPLAY_HEIGHT / 2 - first_text.get_height()
DISPLAY.blit(first_text, (DISPLAY_WIDTH / 2 - first_text.get_width() / 2, text_y))
DISPLAY.blit(second_text, (DISPLAY_WIDTH / 2 - second_text.get_width() / 2, text_y + 100))
if tp:
    DISPLAY.blit(third_text, (DISPLAY_WIDTH / 2 - third_text.get_width() / 2, text_y + 150))
pg.display.update()
sleep(5)

pg.quit()
