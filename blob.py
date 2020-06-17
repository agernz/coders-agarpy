import random as rand
from constants import pg

BLOB_TIERS = {
    1: ((255, 46, 46), 5, 5),
    2: ((18, 255, 18), 3, 4),
    3: ((0, 196, 196), 1, 3)
}


class Blob():

    def __init__(self, init_x, init_y, id):
        self.id = id + 1
        self.rect = None
        self.pos = (init_x, init_y)
        self.tier = rand.randrange(100)
        if self.tier < 10:
            self.color, self.points, self.radius = BLOB_TIERS[1]
        elif self.tier < 20:
            self.color, self.points, self.radius = BLOB_TIERS[2]
        else:
            self.color, self.points, self.radius = BLOB_TIERS[3]

    def get_id(self):
        return self.id

    def get_pos(self):
        return self.pos

    def draw(self, target_surface):
        self.rect = pg.draw.circle(target_surface, self.color, \
                                   self.pos, self.radius)
