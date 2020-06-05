from Player import Player
from constants import pygame, DISPLAY_WIDTH, DISPLAY_HEIGHT


DISPLAY = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption('AgarPy')
BACKGROUND = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
BACKGROUND.fill((33, 33, 33))
DISPLAY.blit(BACKGROUND, (0, 0))

CLOCK = pygame.time.Clock()

def create_text(text, x_pos, y_pos, color, size):
    font_obj = pygame.font.Font('freesansbold.ttf', size)
    textsurface = font_obj.render(text, True, color, (33, 33, 33, 0))
    textsurface.set_colorkey((33, 33, 33))
    text_rect_obj = textsurface.get_rect()
    text_rect_obj.center = (x_pos, y_pos)
    return textsurface, text_rect_obj

def erase_dirty(surf, spr_rect):
    surf.blit(BACKGROUND, spr_rect, spr_rect)

class FPSUtil(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = self.rect = None
        self.update(0)

    def update(self, alpha):
            self.image, self.rect = create_text(str(int(CLOCK.get_fps())),
                                                DISPLAY_WIDTH - 20,
                                                20, (0, 200, 0),
                                                DISPLAY_HEIGHT // 40)


PLAYER = Player(DISPLAY_WIDTH // 2, 800, (30, 101, 150))
ALL_SPRITES = pygame.sprite.Group()
ALL_SPRITES.add(PLAYER)
ALL_SPRITES.add(FPSUtil())


RUNNING = True
DELTA_T = 10
MAX_FRAME_TIME = 250
ACC = 0
controls = [0] * 4
while RUNNING:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                RUNNING = False
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                controls[0] = -1
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                controls[1] = 1
            elif event.key == pygame.K_w or event.key == pygame.K_UP:
                controls[2] = -1
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                controls[3] = 1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                controls[0] = 0
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                controls[1] = 0
            elif event.key == pygame.K_w or event.key == pygame.K_UP:
                controls[2] = 0
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                controls[3] = 0

    if not controls[0] & controls[1]:
        PLAYER.x_velocity = controls[0] or controls[1]
    if not controls[2] & controls[3]:
        PLAYER.y_velocity = controls[2] or controls[3]

    temp = CLOCK.tick()
    if temp > MAX_FRAME_TIME:
        print("ERROR")
    ACC += min(temp, MAX_FRAME_TIME)
    while ACC >= DELTA_T:
        ALL_SPRITES.update(-1)
        ACC -= DELTA_T
    ALL_SPRITES.update(float(ACC) / DELTA_T)

    ALL_SPRITES.clear(DISPLAY, erase_dirty)
    ALL_SPRITES.draw(DISPLAY)
    pygame.display.flip()

pygame.quit()
