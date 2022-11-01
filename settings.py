import math
from enum import Enum

RES = WIDTH, HEIGHT = 1600, 900
HALF_WITH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 60

PLAYER_POS = 1.5, 5
PLAYER_ANGLE = 0
PLAYER_SPEED = 0.004
PLAYER_ROT_SPEED = 0.002
PLAYER_SIZE_SCALE = 60

MOUSE_SENSITIVITY = 0.0003
MOUSE_MAX_REL = 40
MOUSE_BORDER_LEFT = 100
MOUSE_BORDER_RIGHT = WIDTH - MOUSE_BORDER_LEFT

FLOOR_COLOR = (30, 30, 30)

FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = WIDTH // 2
HALF_NUM_RAYS = NUM_RAYS // 2
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 20

SCREEN_DIST = HALF_WITH / math.tan(HALF_FOV)
SCALE = WIDTH // NUM_RAYS

TEXTURE_SIZE = 256
HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2

COLOR_RAY = 'yellow'
COLOR_RAY_RED = 'red'
COLOR_CELL = 'darkgray'
COLOR_PLAYER = 'green'
COLOR_WINDOW_BACK = 'black'
CELL_SIZE = 50

MAP_SHIFT_X = 0
MAP_SHIFT_Y = 0


class RenderType(Enum):
    TwoD = 1
    Walls = 2
    WallsTextures = 3


RENDER_TYPE = RenderType.Walls
