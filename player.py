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
        if decision is not None:
            self.make_decision = decision
            self.isBot = False

    def update_rect(self):
        self.rect = pg.Rect(self.cur_state[0] - self.radius, self.cur_state[1] - self.radius, \
                                self.radius * 2, self.radius * 2)

    def get_player_distance(self, other_player):
        return other_player[2]

    def get_blob_distance(self, blob):
        return blob[1]

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

    def make_decision(self, world):
        direction = [0, 0]
        players = world.get_other_players(self.name)
        closest = players[0]
        distance = self.get_player_distance(closest)
        if distance < 100:
            if self.radius > self.get_player_size(closest):
                direction = self.get_direction(closest)
            elif self.radius < self.get_player_distance(closest):
                direction = self.get_opposite_direction(closest)
            return direction
        else:
            blobs = world.get_blobs(self)
            closest_blob = blobs[0]
            direction = self.get_direction(closest_blob)
            return direction

    def get_state(self):
        return self.cur_state

    def get_name(self):
        return self.name


    def increase_size(self, delta):
        self.radius += delta
        self.update_rect()
        self.velocity = round(self.speed - self.radius / 75.)

    def move(self, direction):
        if direction == 'UP':
            self.y_dir = 1
        elif direction == 'DOWN':
            self.y_dir = -1
        if direction == 'RIGHT':
            self.x_dir = 1
        elif direction == 'LEFT':
            self.x_dir = -1

    def stop(self):
        self.x_dir = 0
        self.y_dir = 0

    def interpolate(self, alpha):
        a = tuple(x * alpha for x in self.cur_state)
        b = tuple(x * (1.0 - alpha) for x in self.prev_state)
        inter_state = (a[0] + b[0], a[1] + b[1])
        self.rect.center = inter_state

    def update(self, world):
        self.prev_state = self.cur_state
        if not self.isBot:
            self.x_dir, self.y_dir = self.make_decision(self, world)
        else:
            self.x_dir, self.y_dir = self.make_decision(world)

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
