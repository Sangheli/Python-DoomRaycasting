import numpy as np

cell1 = (200, 200, 200)
cell2 = (100, 100, 100)
red = (255, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)
black = (0, 0, 0)
wall_color = (175, 75, 0)

backGround = (145, 163, 176)
backSky = (137, 207, 240)

color_reflection = (0, 0, 0, 122)


def get_shading(color, depth):
    return np.array(color) / (1 + depth * depth * 0.00001)
