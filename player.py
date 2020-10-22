import time
from random import randrange
from math import sqrt
from constants import pg, DISPLAY_WIDTH, DISPLAY_HEIGHT, TEXT_COLOR
from pygame import gfxdraw


class Player():
    dec_counter = 0

    def __init__(self, init_x, init_y, color, name, decision=None):
        self.name = name
        self.cur_state = (init_x, init_y)
        self.prev_state = self.cur_state
        self.color = color
        self.radius = 10
        self.x_dir = 0
        self.y_dir = 0
        self.speed = 5
        self.velocity = self.speed
        self.image = None
        self.isBot = True
        font = pg.font.SysFont('chalkduster.ttf', 20)
        self.name_text = font.render(name, True, TEXT_COLOR)
        self.rect = None
        self.update_rect()
        self.nearest_player = None
        self.nearest_food = None
        self.danger_player = None
        if decision is not None:
            self.make_decision = decision
            self.isBot = False

    def update_rect(self):
        self.rect = pg.Rect(self.cur_state[0] - self.radius, self.cur_state[1] - self.radius, \
                                self.radius * 2, self.radius * 2)

    def get_player_distance(self, other_player):
        return other_player[2]

    def get_blob_distance(self, blob):
        return blob[2]

    def get_player_size(self, other_player):
        return other_player[3]

    def get_direction(self, other):
        # returns the in unit vector form to another blob or player
        other_location = other[1]
        x, y = other_location[0] - self.cur_state[0], other_location[1] - self.cur_state[1]
        m = sqrt(x * x + y * y)
        return x / m, y / m

    def get_opposite_direction(self, other_player):
        other_direction = self.get_direction(other_player)
        return other_direction[0] * -1, other_direction[1] * -1

    def increase_size(self, delta):
        max_radius = 100
        self.radius += delta
        if self.radius < max_radius:
            self.update_rect()
            self.velocity = round(self.speed - self.radius / 75.)
        else:
            self.radius = max_radius

    def interpolate(self, alpha):
        a = tuple(x * alpha for x in self.cur_state)
        b = tuple(x * (1.0 - alpha) for x in self.prev_state)
        inter_state = (a[0] + b[0], a[1] + b[1])
        self.rect.center = inter_state

    def is_in_danger(self):
        if self.danger_player:
            return self.get_player_distance(self.danger_player)
        return 0

    def run_away(self):
        if self.danger_player:
            self.x_dir, self.y_dir = self.get_opposite_direction(self.danger_player)
        self.x_dir, self.y_dir = self.get_opposite_direction(self.nearest_player)

    def attack_nearest_player(self):
        if self.nearest_player:
            self.x_dir, self.y_dir = self.get_direction(self.nearest_player)

    def eat_food(self):
        if self.nearest_food:
            self.x_dir, self.y_dir = self.get_direction(self.nearest_food)

    def get_nearest_player_size(self):
        if self.nearest_player:
            return self.get_player_size(self.nearest_player)
        return 0

    def get_nearest_player_distance(self):
        if self.nearest_player:
            return self.get_player_distance(self.nearest_player)
        return 100

    def get_food_ponts(self):
        if self.nearest_food:
            return self.get_blob_distance(self.nearest_food[3])
        return 0

    def get_food_distance(self):
        if self.nearest_food:
            return self.get_blob_distance(self.nearest_food)
        return 0

    def simple_logic(self):
        if self.is_in_danger():
            self.run_away()
        elif self.get_nearest_player_distance() < self.get_food_distance():
            self.attack_nearest_player()
        else:
            self.eat_food()

    def update(self, world):
        self.danger_player = None
        other_players = world.get_other_players(self.name)
        for op in other_players:
            if self.get_player_distance(op) - self.get_player_size(op) <= 100 \
                and self.get_player_size(op) > self.radius:
                self.danger_player = op
                break

        self.nearest_player = other_players[0]
        self.nearest_food = world.get_blobs(self)[0]

        self.prev_state = self.cur_state
        if self.isBot:
            self.simple_logic()
        else:
            self.make_decision(self)

        font = pg.font.SysFont('chalkduster.ttf', 20)
        self.name_text = font.render(self.name, True, TEXT_COLOR)

        self.cur_state = (self.cur_state[0] + self.x_dir * self.velocity, \
                          self.cur_state[1] + self.y_dir * self.velocity)
        if self.cur_state[1] < 0 or self.cur_state[1] > DISPLAY_HEIGHT:
            self.cur_state = (self.cur_state[0], self.prev_state[1])
        if self.cur_state[0] < 0 or self.cur_state[0] > DISPLAY_WIDTH:
            self.cur_state = (self.prev_state[0], self.cur_state[1])
        self.rect.center = self.cur_state

    def draw(self, target_surface):
        pos = tuple([int(x) for x in self.cur_state])
        radius = int(self.radius)
        gfxdraw.filled_circle(target_surface, pos[0], pos[1], radius, self.color)
        gfxdraw.aacircle(target_surface, pos[0], pos[1], radius, self.color)

        # draw a circle to represent the line of sight of the blob
        pg.draw.circle(target_surface, (255, 255, 255), pos, radius + 100, 1)
        text_pos = (
            self.cur_state[0] - self.name_text.get_width() / 2,
            self.cur_state[1] - self.name_text.get_height() / 2
        )
        target_surface.blit(self.name_text, text_pos)
