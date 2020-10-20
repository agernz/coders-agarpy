from constants import pg, ENV
import math

controls = [0, 0, 0, 0]


def process_input(player):
    global controls
    for event in pg.event.get():
        if event.type == pg.QUIT:
            return False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                return False
            if event.key == pg.K_a or event.key == pg.K_LEFT:
                controls[0] = -1
            elif event.key == pg.K_d or event.key == pg.K_RIGHT:
                controls[1] = 1
            elif event.key == pg.K_w or event.key == pg.K_UP:
                controls[2] = -1
            elif event.key == pg.K_s or event.key == pg.K_DOWN:
                controls[3] = 1
        elif event.type == pg.KEYUP:
            if event.key == pg.K_a or event.key == pg.K_LEFT:
                controls[0] = 0
            elif event.key == pg.K_d or event.key == pg.K_RIGHT:
                controls[1] = 0
            elif event.key == pg.K_w or event.key == pg.K_UP:
                controls[2] = 0
            elif event.key == pg.K_s or event.key == pg.K_DOWN:
                controls[3] = 0

    if ENV == 'dev':
        if not controls[0] & controls[1]:
            player.x_dir = controls[0] or controls[1]
        if not controls[2] & controls[3]:
            player.y_dir = controls[2] or controls[3]
    return True


def two_point_distance(point1, point2):
    # return round(math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2),2)
    return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)
