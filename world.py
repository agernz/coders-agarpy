import math
import random as rand
from blob import Blob
from player import Player
from constants import DISPLAY_WIDTH, DISPLAY_HEIGHT, ENV

class World():
    def __init__(self):
        self.players = []
        if ENV == 'dev':
            self.players.append(Player(DISPLAY_WIDTH // 2, 400, (82, 0, 176), "bob"))
        self.blobs = []
        self.add_blobs(150)

    def add_blobs(self, n):
        for i in range(n):
            rand_x = rand.randrange(5, DISPLAY_WIDTH)
            rand_y = rand.randrange(5, DISPLAY_HEIGHT)
            self.blobs.append(Blob(rand_x, rand_y))

    def get_blobs_near_player(self, player):
        pass

    def get_players_near_player(self, player):
        pass

    def is_collided(self, obj1, obj2):
        if obj1.rect is None or obj2.rect is None:
            return False
        obj1_x = obj1.rect.center[0]
        obj1_y = obj1.rect.center[1]
        obj2_x = obj2.rect.center[0]
        obj2_y = obj2.rect.center[1]
        return math.sqrt((obj1_x - obj2_x) ** 2  + (obj1_y - obj2_y) ** 2) <= obj1.radius

    def interpolate(self, alpha):
        for player in self.players:
            player.interpolate(alpha)

    def update(self):
        if len(self.blobs) < 100:
            self.add_blobs(rand.randrange(50, 80))
        for player in self.players:
            player.update()

        for player in self.players:
            for blob in [blob for blob in self.blobs if self.is_collided(player, blob)]:
                player.increase_size(blob.points)
                self.blobs.remove(blob)

    def draw(self, draw_sprites):
        draw_sprites(self.players)
        draw_sprites(self.blobs)
