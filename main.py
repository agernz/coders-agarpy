import math
import random as rand
from player import Player
from blob import Blob
from utils import process_input
from constants import pg, DISPLAY_WIDTH, DISPLAY_HEIGHT, ENV


def is_collided(obj1, obj2):
    obj1_x = obj1.rect.center[0]
    obj1_y = obj1.rect.center[1]
    obj2_x = obj2.rect.center[0]
    obj2_y = obj2.rect.center[1]
    return math.sqrt((obj1_x - obj2_x) ** 2  + (obj1_y - obj2_y) ** 2) <= obj1.radius


def player_blobs_collide(player, blobs):
    return [blob for blob in blobs if is_collided(player, blob)]


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

# world setup
players = []
players.append(Player(DISPLAY_WIDTH // 2, 400, (82, 0, 176), "bob"))

point_blobs = []
for i in range(150):
    rand_x = rand.randrange(10, DISPLAY_WIDTH)
    rand_y = rand.randrange(10, DISPLAY_HEIGHT)
    point_blobs.append(Blob(rand_x, rand_y))

# initial draw
DISPLAY.blit(BACKGROUND, (0, 0))
draw_sprites(players)
draw_sprites(point_blobs)

while running:
    running = process_input(players[0])

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
        for player in players:
            player.update()
        acc -= DELTA_T
    for player in players:
        player.interpolate(float(acc) / DELTA_T)

    for player in players:
        for blob in player_blobs_collide(player, point_blobs):
            player.increase_size(blob.points)
            point_blobs.remove(blob)

    DISPLAY.blit(BACKGROUND, (0, 0))
    draw_sprites(players)
    draw_sprites(point_blobs)
    pg.display.update()

pg.quit()
