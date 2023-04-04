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


def get_shading(color, depth):
    return np.array(color) / (1 + depth * depth * 0.0001)


def get_fixed_fisheye_depth(depth, angle):
    return depth * math.cos(_var_.player_angle - angle)


def get_wall_sector_height(depth, angle):
    depth = get_fixed_fisheye_depth(depth, angle)
    wall_sector_height_PX = 21000 / (depth + 0.0001)
    if wall_sector_height_PX > _var_.SCREEN_HEIGHT: wall_sector_height_PX == _var_.SCREEN_HEIGHT
    return wall_sector_height_PX


def get_wall_segment_rect(ray, wall_sector_height_PX):
    screen_pos_x = _var_.SCREEN_HEIGHT + ray * _var_.WALL_SECTOR_SIZE_PX;
    screen_pos_Y = _var_.SCREEN_HEIGHT / 2 - wall_sector_height_PX / 2;
    return screen_pos_x, screen_pos_Y, _var_.WALL_SECTOR_SIZE_PX, wall_sector_height_PX


def draw_3D_wall_segment(ray, depth, angle):
    color = get_shading(_color_.wall_color, depth)
    wall_sector_height_PX = get_wall_sector_height(depth, angle)
    rect = get_wall_segment_rect(ray, wall_sector_height_PX)
    pygame.draw.rect(_var_.win, color, rect)
