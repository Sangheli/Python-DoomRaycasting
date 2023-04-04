import pygame
import sys
import math
import simple_raycast.color as my

pygame.init()

forward = True
draw2D = True

SCREEN_HEIGHT = 480

MULT_SCREEN_WIDTH = 2 if draw2D else 1
SHIFT_WIDTH = SCREEN_HEIGHT if draw2D else 0

SCREEN_WIDTH = SCREEN_HEIGHT * MULT_SCREEN_WIDTH
MAP_SIZE = 8
TILE_SIZE = ((SCREEN_WIDTH / 2 ) / MAP_SIZE)
MAX_DEPTH = int(MAP_SIZE * TILE_SIZE)
FOV = math.pi / 3
HALF_FOV = FOV / 2
CASTED_RAYS = 120
STEP_ANGLE = FOV / CASTED_RAYS
SCALE = (SCREEN_WIDTH / 2) / CASTED_RAYS

player_x = (SCREEN_WIDTH / 2) / 2
player_y = (SCREEN_WIDTH / 2) / 2
player_angle = math.pi

wallID = "#"

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Raycasting by Network Skeleton")
clock = pygame.time.Clock()

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

def draw_2D_cell(col,row):
    index = row * MAP_SIZE + col
    cur_color = my.cell1 if MAP[index] == wallID else my.cell2
    pygame.draw.rect(win, cur_color, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2))

def draw_2D_player_base_rays():
    pygame.draw.line(win, my.green, (player_x, player_y),
                     (player_x - math.sin(player_angle) * 50, player_y + math.cos(player_angle) * 50), 3)
    pygame.draw.line(win, my.green, (player_x, player_y), (
        player_x - math.sin(player_angle - HALF_FOV) * 50, player_y + math.cos(player_angle - HALF_FOV) * 50), 3)
    pygame.draw.line(win, my.green, (player_x, player_y), (
        player_x - math.sin(player_angle + HALF_FOV) * 50, player_y + math.cos(player_angle + HALF_FOV) * 50), 3)

def draw_2D_map():
    if not draw2D: return

    #back
    pygame.draw.rect(win, (0, 0, 0), (0, 0, SCREEN_HEIGHT, SCREEN_HEIGHT))

    #cells
    for row in range(MAP_SIZE):
        for col in range(MAP_SIZE):
            draw_2D_cell(col,row)

    #player dot
    pygame.draw.circle(win, my.red, (int(player_x), int(player_y)), 8)
    draw_2D_player_base_rays()

def draw_2D_rays(col, row, target_x, target_y):
    if not draw2D: return
    pygame.draw.rect(win, my.green, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2))
    pygame.draw.line(win, my.yellow, (player_x, player_y), (target_x, target_y))

def draw_3D_back():
    pygame.draw.rect(win, (100, 0, 0), (SHIFT_WIDTH, SCREEN_HEIGHT / 2, SCREEN_HEIGHT, SCREEN_HEIGHT))
    pygame.draw.rect(win, (200, 0, 0), (SHIFT_WIDTH, -SCREEN_HEIGHT / 2, SCREEN_HEIGHT, SCREEN_HEIGHT))

def draw_3D_wall_segment(ray, depth, start_angle):
    color = 50 / (1 + depth * depth * 0.0001)
    depth *= math.cos(player_angle - start_angle)
    wall_height = 21000 / (depth + 0.0001)
    if wall_height > SCREEN_HEIGHT: wall_height == SCREEN_HEIGHT

    pygame.draw.rect(win, (color, color, color), (
        SCREEN_HEIGHT + ray * SCALE, (SCREEN_HEIGHT / 2) - wall_height / 2, SCALE, wall_height))

def cast_rays():
    start_angle = player_angle - HALF_FOV

    for ray in range(CASTED_RAYS):
        for depth in range(MAX_DEPTH):
            target_x = player_x - math.sin(start_angle) * depth
            target_y = player_y + math.cos(start_angle) * depth
            col = int(target_x / TILE_SIZE)
            row = int(target_y / TILE_SIZE)
            index = row * MAP_SIZE + col

            if MAP[index] == wallID:
                draw_2D_rays(col, row, target_x, target_y)
                draw_3D_wall_segment(ray, depth, start_angle)
                break

        start_angle += STEP_ANGLE

def check_collission(player_x,player_y):
    col = int(player_x / TILE_SIZE)
    row = int(player_y / TILE_SIZE)
    index = row * MAP_SIZE + col

    if MAP[index] == wallID:
        if forward == True:
            player_x -= -math.sin(player_angle) * 5
            player_y -= math.cos(player_angle) * 5
        else:
            player_x += -math.sin(player_angle) * 5
            player_y += math.cos(player_angle) * 5

    return player_x,player_y

def input_scan(player_angle,player_x,player_y,forward):
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

    return player_angle,player_x,player_y,forward

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    player_x,player_y = check_collission(player_x,player_y)
    draw_2D_map()
    draw_3D_back()
    cast_rays()
    player_angle,player_x,player_y,forward = input_scan(player_angle,player_x,player_y,forward)
    clock.tick(60)
    fps = str(int(clock.get_fps()))
    font = pygame.font.SysFont('Monospace Regular', 30)
    textsurface = font.render(fps, False, (255, 255, 255))
    win.blit(textsurface, (0, 0))
    pygame.display.flip()
