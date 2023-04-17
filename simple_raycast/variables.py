import math
import pygame
import numpy as np

draw2D = True

# Map parameters
TILE_SIZE = 60
MAP_SIZE = 8

# render parameters
SCREEN_WIDTH, SCREEN_HEIGHT = 480, 480
HALF_HEIGHT = SCREEN_HEIGHT // 2
SCREEN_START = np.array([SCREEN_WIDTH if draw2D else 0, SCREEN_HEIGHT / 2])
TILE_MULT = SCREEN_WIDTH/480
TILE_SIZE_2D = TILE_MULT * TILE_SIZE

CASTED_RAYS = 240
MAX_DEPTH = int(MAP_SIZE * TILE_SIZE)

WALL_SECTOR_PX   = SCREEN_WIDTH / CASTED_RAYS
WALL_HEIGHT_PROJ_COEF = 21000 * SCREEN_HEIGHT / 480

# Player setup
forward = True
player_x, player_y, player_angle = 1.5 * TILE_SIZE, 6.5 * TILE_SIZE,0

PLAYER_SPEED = 200
PLAYER_ROT_SPEED = 5

FOV = math.pi / 3
HALF_FOV = FOV / 2
STEP_ANGLE = FOV / CASTED_RAYS

SCREEN_DIST = SCREEN_WIDTH//2 / math.tan(HALF_FOV)

# Game params
DRAW_REFLECTION = True
DRAW_TEXTURE = True
SHADE_TEXTURE = True
DRAW_SKY = True
DRAW_AO = True
DRAW_FLOOR_TX = True

SCREEN_MULT = 2
# Game
rect_main_frame = np.array([int(SCREEN_WIDTH + SCREEN_START[0]), SCREEN_HEIGHT, 3])
rect_main_frame_scaled = np.array([int(SCREEN_WIDTH + SCREEN_START[0]), SCREEN_HEIGHT, 3])*SCREEN_MULT
win = pygame.display.set_mode((SCREEN_WIDTH * (2 if draw2D else 1)*SCREEN_MULT, SCREEN_HEIGHT*SCREEN_MULT))
pygame.display.set_caption("Raycasting by Sangheli")
