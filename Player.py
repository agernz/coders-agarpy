from constants import pg, DISPLAY_WIDTH, DISPLAY_HEIGHT


class Player():

    def __init__(self, init_x, init_y, color, name):
        self.cur_state = (init_x, init_y)
        self.prev_state = self.cur_state
        self.color = color
        self.radius = 10
        self.x_dir = 0
        self.y_dir = 0
        self.speed = 9
        self.velocity = self.speed
        self.image = None
        self.rect = None
        font = pg.font.SysFont('chalkduster.ttf', 20)
        self.name_text = font.render(name, True, (255, 255, 255))

    def increase_size(self, delta):
        self.radius += delta
        if self.velocity > 1:
            self.velocity = round(self.speed - self.radius / 30.)

    def move(self, direciton):
        if direciton == 'UP':
            self.y_dir = 1
        elif direciton == 'DOWN':
            self.y_dir = -1
        if direciton == 'RIGHT':
            self.x_dir = 1
        elif direciton == 'LEFT':
            self.x_dir = -1

    def stop(self):
        self.x_dir = 0
        self.y_dir = 0

    def interpolate(self, alpha):
        a = tuple(x * alpha for x in self.cur_state)
        b = tuple(x * (1.0 - alpha) for x in self.prev_state)
        inter_state = (a[0] + b[0], a[1] + b[1])
        self.rect.center = inter_state

    def update(self):
        self.prev_state = self.cur_state
        self.cur_state = (self.cur_state[0] + self.x_dir * self.velocity, \
            self.cur_state[1] + self.y_dir * self.velocity)
        if self.cur_state[1] < 0 or self.cur_state[1] > DISPLAY_HEIGHT:
            self.cur_state = (self.cur_state[0], self.prev_state[1])
        if self.cur_state[0] < 0 or self.cur_state[0] > DISPLAY_WIDTH:
            self.cur_state = (self.prev_state[0], self.cur_state[1])
        self.rect.center = self.cur_state

    def draw(self, target_surface):
        self.rect = pg.draw.circle(target_surface, self.color, \
            self.cur_state, self.radius)
        text_pos = (
            self.cur_state[0] - self.name_text.get_width() / 2,
            self.cur_state[1] - self.name_text.get_height() / 2
        )
        target_surface.blit(self.name_text, text_pos)
