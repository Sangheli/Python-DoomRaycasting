import math
import pygame

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