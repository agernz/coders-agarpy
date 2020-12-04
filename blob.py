import random as rand
from constants import pg
from pygame import gfxdraw


FILL_COLOR = (181, 101, 118)
OUTLINE_COLOR = (94, 100, 114)
BLOB_TIERS = {
    1: (3, 5),
    2: (2, 4),
    3: (1, 3)
}


class Blob():

    def __init__(self, init_x, init_y, id):
        self.id = id + 1
        self.pos = (init_x, init_y)
        self.tier = rand.randrange(100)
        if self.tier < 10:
            self.points, self.radius = BLOB_TIERS[1]
        elif self.tier < 20:
            self.points, self.radius = BLOB_TIERS[2]
        else:
            self.points, self.radius = BLOB_TIERS[3]
        self.rect = pg.Rect(self.pos[0] - self.radius, self.pos[1] - self.radius, \
                                self.radius * 2, self.radius * 2)

    def draw(self, target_surface):
        gfxdraw.filled_circle(target_surface, self.pos[0], self.pos[1], self.radius, FILL_COLOR)
        gfxdraw.aacircle(target_surface, self.pos[0], self.pos[1], self.radius, OUTLINE_COLOR)
