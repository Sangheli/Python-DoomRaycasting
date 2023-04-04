import pygame
import sys
import math

pygame.init()

SCREEN_HEIGHT = 480
SCREEN_WIDTH = SCREEN_HEIGHT * 2
MAP_SIZE = 8
TILE_SIZE = ((SCREEN_WIDTH / 2) / MAP_SIZE)
MAX_DEPTH = int(MAP_SIZE * TILE_SIZE)
FOV = math.pi / 3
HALF_FOV = FOV / 2
CASTED_RAYS = 120
STEP_ANGLE = FOV / CASTED_RAYS
SCALE = (SCREEN_WIDTH / 2) / CASTED_RAYS

player_x = (SCREEN_WIDTH / 2) / 2
player_y = (SCREEN_WIDTH / 2) / 2
player_angle = math.pi

MAP = (
    '########'
    '#   ## #'
    '#      #'
    '#    ###'
    '##     #'
    '#   #  #'
    '#   #  #'
    '########'
)

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Raycasting by Network Skeleton")

clock = pygame.time.Clock()


def draw_map():
    for row in range(8):
        for col in range(8):
            square = row * MAP_SIZE + col

            pygame.draw.rect(
                win,
                (200, 200, 200) if MAP[square] == '#' else (100, 100, 100),
                (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2)

            )
    pygame.draw.circle(win, (255, 0, 0), (int(player_x), int(player_y)), 8)
    pygame.draw.line(win, (0, 255, 0), (player_x, player_y),
                     (player_x - math.sin(player_angle) * 50, player_y + math.cos(player_angle) * 50), 3)
    pygame.draw.line(win, (0, 255, 0), (player_x, player_y), (
    player_x - math.sin(player_angle - HALF_FOV) * 50, player_y + math.cos(player_angle - HALF_FOV) * 50), 3)
    pygame.draw.line(win, (0, 255, 0), (player_x, player_y), (
    player_x - math.sin(player_angle + HALF_FOV) * 50, player_y + math.cos(player_angle + HALF_FOV) * 50), 3)


def cast_rays():
    start_angle = player_angle - HALF_FOV

    for ray in range(CASTED_RAYS):
        for depth in range(MAX_DEPTH):
            target_x = player_x - math.sin(start_angle) * depth
            target_y = player_y + math.cos(start_angle) * depth
            col = int(target_x / TILE_SIZE)
            row = int(target_y / TILE_SIZE)

            square = row * MAP_SIZE + col
            (target_y / TILE_SIZE) * MAP_SIZE + target_x / TILE_SIZE
            if MAP[square] == '#':
                pygame.draw.rect(win, (0, 255, 0), (col * TILE_SIZE,
                                                    row * TILE_SIZE,
                                                    TILE_SIZE - 2,
                                                    TILE_SIZE - 2))
                pygame.draw.line(win, (255, 255, 0), (player_x, player_y), (target_x, target_y))
                color = 50 / (1 + depth * depth * 0.0001)

                depth *= math.cos(player_angle - start_angle)

                wall_height = 21000 / (depth + 0.0001)

                if wall_height > SCREEN_HEIGHT: wall_height == SCREEN_HEIGHT

                pygame.draw.rect(win, (color, color, color), (
                SCREEN_HEIGHT + ray * SCALE, (SCREEN_HEIGHT / 2) - wall_height / 2, SCALE, wall_height))

                break

        start_angle += STEP_ANGLE


forward = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    col = int(player_x / TILE_SIZE)
    row = int(player_y / TILE_SIZE)

    square = row * MAP_SIZE + col
    (player_y / TILE_SIZE) * MAP_SIZE + player_x / TILE_SIZE
    if MAP[square] == '#':
        if forward == True:
            player_x -= -math.sin(player_angle) * 5
            player_y -= math.cos(player_angle) * 5
        else:
            player_x += -math.sin(player_angle) * 5
            player_y += math.cos(player_angle) * 5

    pygame.draw.rect(win, (0, 0, 0), (0, 0, SCREEN_HEIGHT, SCREEN_HEIGHT))

    pygame.draw.rect(win, (100, 0, 0), (480, SCREEN_HEIGHT / 2, SCREEN_HEIGHT, SCREEN_HEIGHT))
    pygame.draw.rect(win, (200, 0, 0), (480, -SCREEN_HEIGHT / 2, SCREEN_HEIGHT, SCREEN_HEIGHT))

    draw_map()
    cast_rays()
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]: player_angle -= 0.1
    if keys[pygame.K_RIGHT]: player_angle += 0.1
    if keys[pygame.K_UP]:
        forward = True
        player_x += -math.sin(player_angle) * 5
        player_y += math.cos(player_angle) * 5
    if keys[pygame.K_DOWN]:
        forward = False
        player_x -= -math.sin(player_angle) * 5
        player_y -= math.cos(player_angle) * 5

    clock.tick(60)

    fps = str(int(clock.get_fps()))
    font = pygame.font.SysFont('Monospace Regular', 30)
    textsurface = font.render(fps, False, (255, 255, 255))
    win.blit(textsurface, (0, 0))
    pygame.display.flip()