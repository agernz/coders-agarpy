import math
import random as rand
from blob import Blob
from player import Player
from utils import two_point_distance
from updatePlayer import PLAYER_NAME, update_player
from constants import DISPLAY_WIDTH, DISPLAY_HEIGHT, PLAYER_COLORS


class World():
    player_distances = {}
    player_to_blob_distances = {}
    locations = {}

    def __init__(self):
        self.players = []
        colors = list(PLAYER_COLORS.values())
        human = Player(rand.randrange(DISPLAY_WIDTH),
                       rand.randrange(DISPLAY_HEIGHT),
                       colors[0],
                       PLAYER_NAME,
                       decision=update_player)
        self.players.append(human)
        # just populate 1 bot
        for i in range(1,2):
            self.players.append(Player(rand.randrange(DISPLAY_WIDTH),
                                       rand.randrange(DISPLAY_HEIGHT),
                                       rand.choice(colors[1:]),
                                       "BOT"))
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
                name_a = player_a.name
                name_b = player_b.name
                if name_a != name_b:
                    distance = two_point_distance(player_a.cur_state, player_b.cur_state)
                    if name_a not in self.player_distances:
                        self.player_distances[name_a] = []
                    self.player_distances[name_a].append((
                        player_b.name, player_b.cur_state, distance, player_b.radius))

    def calculate_player_blob_distances(self):
        for player_a in self.players:
            for blob in self.blobs:
                name_a = player_a.name
                if name_a not in self.player_to_blob_distances:
                    self.player_to_blob_distances[name_a] = []
                distance = two_point_distance(player_a.cur_state, blob.pos)
                self.player_to_blob_distances[name_a].append((
                    blob.id, blob.pos, distance, blob.points))

    def get_other_players(self, player_name):
        return sorted(list(self.player_distances[player_name]), key=lambda p: p[2])

    def get_blobs(self, player):
        return sorted(list(self.player_to_blob_distances[player.name]), key=lambda p: p[2])

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

    def update(self):
        self.locations.clear()
        self.player_distances.clear()
        self.player_to_blob_distances.clear()
        self.calculate_player_distances()
        self.calculate_player_blob_distances()
        self.get_locations()
        if len(self.blobs) < 50:
            self.add_blobs(50 - len(self.blobs))
        for player in self.players:
            player.update(self)

        for player in self.players:
            for blob in [blob for blob in self.blobs if self.is_collided(player, blob)]:
                player.increase_size(blob.points)
                self.blobs.remove(blob)
            for player2 in self.players:
                if player == player2:
                    continue
                if self.is_collided(player, player2):
                    if player.radius > player2.radius:
                        player.increase_size(player2.radius / 5)
                        player2.cur_state = rand.randrange(DISPLAY_WIDTH), \
                            rand.randrange(DISPLAY_HEIGHT)
                        player2.radius = 10
                        player2.decrease_score()
                    else:
                        # tie breaker needed, randomly pick one to eat since same size
                        if rand.random() > .49:
                            player.increase_size(player2.radius / 5)
                            player2.cur_state = rand.randrange(DISPLAY_WIDTH), \
                                rand.randrange(DISPLAY_HEIGHT)
                            player2.decrease_score()
                            player2.radius = 10
                        else:
                            player2.increase_size(player.radius / 5)
                            player.cur_state = rand.randrange(DISPLAY_WIDTH), \
                                rand.randrange(DISPLAY_HEIGHT)
                            player.decrease_score()
                            player.radius = 10

    def get_top_players(self):
        top_players = sorted(self.players, key=lambda player: player.score, reverse=True)[:3]
        return (top_player for top_player in top_players)

    def draw(self, draw_sprites):
        draw_sprites(self.players)
        draw_sprites(self.blobs)
