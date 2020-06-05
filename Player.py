from constants import pygame, DISPLAY_WIDTH, DISPLAY_HEIGHT, COLORKEY


class Player(pygame.sprite.Sprite):

    def __init__(self, init_x, init_y, color):
        pygame.sprite.Sprite.__init__(self)
        self.cur_state = (init_x, init_y)
        self.prev_state = self.cur_state
        self.color = color
        self.radius = 30
        self.x_velocity = 0
        self.y_velocity = 0
        self.image = None
        self.rect = None
        self.draw_circle()

    def draw_circle(self):
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        self.image.fill(COLORKEY)
        self.image.set_colorkey(COLORKEY)
        self.rect = pygame.draw.circle(self.image, self.color, \
            (self.radius, self.radius), self.radius)

    def increase_size(self, radius_delta):
        self.radius += radius_delta
        self.draw_circle()

    def update(self, alpha):
        if alpha != -1:
            a = tuple(x * alpha for x in self.cur_state)
            b = tuple(x * (1.0 - alpha) for x in self.prev_state)
            inter_state = (a[0] + b[0], a[1] + b[1])
            self.rect.center = inter_state
        else:
            self.prev_state = self.cur_state
            self.cur_state = (self.cur_state[0] + self.x_velocity, \
                self.cur_state[1] + self.y_velocity)
            if self.rect.top < 0 or self.rect.bottom > DISPLAY_HEIGHT:
                self.cur_state = (self.cur_state[0], self.prev_state[1])
            if self.rect.left < 0 or self.rect.right > DISPLAY_WIDTH:
                self.cur_state = (self.prev_state[0], self.cur_state[1])
            self.rect.center = self.cur_state
