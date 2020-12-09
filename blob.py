import random as rand
from constants import pg


BLOB_TIERS = {
    1: (3, 6),
    2: (2, 4),
    3: (1, 2)
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
                                self.radius << 1, self.radius << 1)
