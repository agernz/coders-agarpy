import math
import random as rand
from blob import Blob
from player import Player
from constants import DISPLAY_WIDTH, DISPLAY_HEIGHT, ENV
from utils import two_point_distance
from playerloader import get_blobs
from random import randrange


# def random_dec(*paras):
#     return randrange(-1, 2), randrange(-1, 2)


class World():
    player_distances = {}
    player_to_blob_distances = {}
    locations = {}

    def __init__(self):
        self.players = []
        player_blobs = get_blobs()
        for player in player_blobs:
            self.players.append(Player(rand.randrange(DISPLAY_WIDTH),
                                       rand.randrange(DISPLAY_HEIGHT),
                                       (255, 0, 0),
                                       player,
                                       player_blobs[player]))
        self.players.append(Player(rand.randrange(DISPLAY_WIDTH), rand.randrange(DISPLAY_HEIGHT), (0, 0, 255), "bob3"))
        self.players.append(Player(rand.randrange(DISPLAY_WIDTH), rand.randrange(DISPLAY_HEIGHT), (82, 0, 176), "bob4"))
        self.players.append(Player(rand.randrange(DISPLAY_WIDTH), rand.randrange(DISPLAY_HEIGHT), (0, 0, 255), "bob5"))
        self.players.append(Player(rand.randrange(DISPLAY_WIDTH), rand.randrange(DISPLAY_HEIGHT), (82, 0, 176), "bob6"))
        self.blobs = []
        self.add_blobs(50)

    def add_blobs(self, n):
        for i in range(n):
            rand_x = rand.randrange(5, DISPLAY_WIDTH)
            rand_y = rand.randrange(5, DISPLAY_HEIGHT)
            self.blobs.append(Blob(rand_x, rand_y, i))

    def calculate_player_distances(self):
        for player_a in self.players:
            for player_b in self.players:
                name_a = player_a.get_name()
                name_b = player_b.get_name()
                if name_a != name_b:
                    distance = two_point_distance(player_a.get_state(), player_b.get_state())
                    if name_a not in self.player_distances:
                        self.player_distances[name_a] = []
                    self.player_distances[name_a].append((player_b.name, player_b.cur_state, distance, player_b.radius))

    def calculate_player_blob_distances(self):
        for player_a in self.players:
            for blob in self.blobs:
                name_a = player_a.get_name()
                blob_id = str(blob.get_id())
                if name_a not in self.player_to_blob_distances:
                    self.player_to_blob_distances[name_a] = []
                position = blob.get_pos()
                distance = two_point_distance(player_a.get_state(), position)
                self.player_to_blob_distances[name_a].append((blob.get_id(), position, distance))

    def get_other_players(self, player):
        return sorted(list(self.player_distances[player.name]), key=lambda p: p[2])

    def get_blobs(self, player):
        return sorted(list(self.player_to_blob_distances[player.name]), key=lambda p: p[1])

    def get_locations(self):
        for player in self.players:
            self.locations[player.name] = player.cur_state

    def get_player_location(self, player):
        return self.locations[player['name']]

    def is_collided(self, obj1, obj2):
        if obj1.rect is None or obj2.rect is None:
            return False
        obj1_x = obj1.rect.center[0]
        obj1_y = obj1.rect.center[1]
        obj2_x = obj2.rect.center[0]
        obj2_y = obj2.rect.center[1]
        return math.sqrt((obj1_x - obj2_x) ** 2 + (obj1_y - obj2_y) ** 2) <= obj1.radius

    def interpolate(self, alpha):
        for player in self.players:
            player.interpolate(alpha)

    cycle = 0

    def update(self):
        # if self.cycle == 0:
        #     cycle = 10
        self.locations.clear()
        self.player_distances.clear()
        self.player_to_blob_distances.clear()
        self.calculate_player_distances()
        self.calculate_player_blob_distances()
        self.get_locations()
        # self.cycle -= 1
        if len(self.blobs) < 50:
            self.add_blobs(50 - len(self.blobs))
        for player in self.players:
            player.update(self)

        for player in self.players:
            for blob in [blob for blob in self.blobs if self.is_collided(player, blob)]:
                player.increase_size(blob.points)
                self.blobs.remove(blob)
            for player2 in self.players:
                if self.is_collided(player, player2):
                    if player.radius > player2.radius:
                        player.increase_size(player2.radius / 5)
                        player2.cur_state = rand.randrange(DISPLAY_WIDTH), rand.randrange(DISPLAY_HEIGHT)
                        player2.radius = 10
                    elif player2.radius < player.radius:
                        player2.increase_size(player.radius / 5)
                        player.cur_state = rand.randrange(DISPLAY_WIDTH), rand.randrange(DISPLAY_HEIGHT)
                        player.radius = 10

    def draw(self, draw_sprites):
        draw_sprites(self.players)
        draw_sprites(self.blobs)
