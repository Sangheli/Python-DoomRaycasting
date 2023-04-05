import math
import pygame
import numpy as np

draw2D = True

# Map parameters
TILE_SIZE = 60
MAP_SIZE = 8

# render parameters
SCREEN_WIDTH, SCREEN_HEIGHT = 480, 480
SCREEN_START = np.array([SCREEN_WIDTH if draw2D else 0, SCREEN_HEIGHT / 2])
TILE_MULT = SCREEN_WIDTH/480
TILE_SIZE_2D = TILE_MULT * TILE_SIZE

CASTED_RAYS = 120
MAX_DEPTH = int(MAP_SIZE * TILE_SIZE)

WALL_SECTOR_PX   = SCREEN_WIDTH / CASTED_RAYS
WALL_HEIGHT_BASE = 21000 * SCREEN_HEIGHT / 480

# Player setup
forward = True
player_x, player_y, player_angle = 4 * TILE_SIZE, 4 * TILE_SIZE, math.pi

FOV = math.pi / 3
HALF_FOV = FOV / 2
STEP_ANGLE = FOV / CASTED_RAYS

# Game
win = pygame.display.set_mode((SCREEN_WIDTH * (2 if draw2D else 1), SCREEN_HEIGHT))
pygame.display.set_caption("Raycasting by Network Skeleton")
