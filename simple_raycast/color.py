import numpy as np

cell1 = (200, 200, 200)
cell2 = (100, 100, 100)
red = (255, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)
black = (0, 0, 0)
blackA = (0, 0, 0,60)
wall_color = (175, 75, 0)

backGround = (145, 163, 176)
backSky = (137, 207, 240)

color_reflection = (0, 0, 0, 122)


def update_color_shading(color, depth):
    return np.array(color) / get_shading(depth)


def get_color_with_shading(color, shading):
    return np.array(color) / shading


def get_shading(depth):
    return 1 + depth * depth * 0.00001
