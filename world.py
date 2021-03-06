import math
import random as rand
from blob import Blob
from player import Player
from time import time, sleep
from updatePlayer import PLAYER_NAME, update_player
from constants import DISPLAY_WIDTH, DISPLAY_HEIGHT


def get_random_colors(n):
    colors = []
    for i in range(n):
        colors.append(str(hex(rand.randint(0, 16777215)))[-6:])
    return colors


class World():
    player_distances = {}
    player_to_blob_distances = {}
    locations = {}

    def __init__(self):
        colors = get_random_colors(11)
        self.end_time = time() + 180
        self.max_food = 30
        self.players = []
        self.top_player_name = None
        self.running = True
        self.blobs = []
        self.add_blobs(self.max_food)
        human = Player(rand.randrange(DISPLAY_WIDTH),
                       rand.randrange(DISPLAY_HEIGHT),
                       PLAYER_NAME,
                       colors[0],
                       decision=update_player)
        self.players.append(human)
        for i in range(1, 4):
            self.players.append(Player(rand.randrange(DISPLAY_WIDTH),
                                       rand.randrange(DISPLAY_HEIGHT),
                                       'BOT_' + str(i),
                                       colors[i]))

    def restart(self):
        colors = get_random_colors(11)
        self.running = True
        self.end_time = time() + 180
        self.players = []
        self.top_player_name = None
        self.blobs = []
        self.add_blobs(self.max_food)
        human = Player(rand.randrange(DISPLAY_WIDTH),
                       rand.randrange(DISPLAY_HEIGHT),
                       PLAYER_NAME,
                       colors[0],
                       decision=update_player)
        self.players.append(human)
        for i in range(1, 4):
            self.players.append(Player(rand.randrange(DISPLAY_WIDTH),
                                       rand.randrange(DISPLAY_HEIGHT),
                                       'BOT_' + str(i),
                                       colors[i]))

    def get_distance(self, point1, point2):
        return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

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
                    distance = self.get_distance(player_a.cur_state, player_b.cur_state)
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
                distance = self.get_distance(player_a.cur_state, blob.cur_state)
                self.player_to_blob_distances[name_a].append((
                    blob.id, blob.cur_state, distance, blob.points))

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
        obj1_x = obj1.cur_state[0]
        obj1_y = obj1.cur_state[1]
        obj2_x = obj2.cur_state[0]
        obj2_y = obj2.cur_state[1]
        return math.sqrt((obj1_x - obj2_x) ** 2 + (obj1_y - obj2_y) ** 2) <=\
               (obj1.radius + obj2.radius - 4)

    def update(self):
        sleep(.1)
        game_state = {'running': True}
        if time() > self.end_time:
            self.running = False
            game_state['top_player'] = self.top_player_name
            game_state['running'] = self.running
            return game_state

        self.locations.clear()
        self.player_distances.clear()
        self.player_to_blob_distances.clear()
        self.calculate_player_distances()
        self.calculate_player_blob_distances()
        self.get_locations()
        if len(self.blobs) < self.max_food:
            self.add_blobs(self.max_food - len(self.blobs))
        for player in self.players:
            player.update(self)

        player_states = []
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
            player_states.append({
                'x': player.cur_state[0],
                'y': player.cur_state[1],
                'radius': player.radius,
                'name': player.name,
                'color': player.color,
                'score': player.score
            })
        game_state['player_data'] = sorted(player_states,
                                           key=lambda player: player['score'], reverse=True)
        self.top_player_name = game_state['player_data'][0]['name']
        game_state['food_data'] = [(food.cur_state[0], food.cur_state[1], food.radius)
                                   for food in self.blobs]
        game_state['timer'] = int(self.end_time - time())
        return game_state
