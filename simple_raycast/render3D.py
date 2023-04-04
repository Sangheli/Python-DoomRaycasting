import pygame
import math
import simple_raycast.variables as _var_
import simple_raycast.color as _color_
import numpy as np


def draw_3D_back():
    pygame.draw.rect(_var_.win, (100, 0, 0),
                     (_var_.SHIFT_WIDTH, _var_.SCREEN_HEIGHT / 2, _var_.SCREEN_HEIGHT, _var_.SCREEN_HEIGHT))
    pygame.draw.rect(_var_.win, (200, 0, 0),
                     (_var_.SHIFT_WIDTH, -_var_.SCREEN_HEIGHT / 2, _var_.SCREEN_HEIGHT, _var_.SCREEN_HEIGHT))


def draw_3D_wall_segment(ray, depth, start_angle):
    color = np.array(_color_.wall_color) / (1 + depth * depth * 0.0001)
    depth *= math.cos(_var_.player_angle - start_angle)
    wall_height = 21000 / (depth + 0.0001)
    if wall_height > _var_.SCREEN_HEIGHT: wall_height == _var_.SCREEN_HEIGHT

    pygame.draw.rect(_var_.win, color, (
        _var_.SCREEN_HEIGHT + ray * _var_.SCALE, (_var_.SCREEN_HEIGHT / 2) - wall_height / 2, _var_.SCALE, wall_height))
