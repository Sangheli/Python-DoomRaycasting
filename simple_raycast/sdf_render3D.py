import pygame
import math
import variables as _var_
import color as _color_
import numpy as np
from numba import njit
import reflection as _reflection_

@njit(fastmath=True, cache=True)
def get_fixed_fisheye_depth(depth, player_angle, angle):
    return depth * math.cos(player_angle - angle)


@njit(fastmath=True)
def get_wall_segment(ray, proj_height):
    height = min(int(proj_height), _var_.SCREEN_HEIGHT)
    screen_pos_x = ray * _var_.WALL_SECTOR_PX;
    screen_pos_Y = height / 2;
    return np.array([screen_pos_x, screen_pos_Y, _var_.WALL_SECTOR_PX, height])


@njit(fastmath=True)
def get_screen_rect(ray,proj_height):
    rect = get_wall_segment(ray, proj_height)
    shift = _var_.SCREEN_START + np.array([rect[0], -rect[1]])
    return np.array([shift[0], shift[1], rect[2], rect[3]])


def draw_wall_solid_color(frame, rect, shading):
    color = _color_.get_color_with_shading(_color_.wall_color, shading)
    pygame.draw.rect(frame, color, rect)

def draw_3D_wall_segment(frame, ray, depth, angle):
    proj_height = _var_.SCREEN_DIST / (
            get_fixed_fisheye_depth(depth / _var_.TILE_SIZE, _var_.player_angle, angle) + 0.0001)

    screen_rect = get_screen_rect(ray, proj_height)
    shading = _color_.get_shading(depth)
    draw_wall_solid_color(frame,screen_rect, shading)

    if _var_.DRAW_REFLECTION:
        _reflection_.draw_reflection(frame, screen_rect, shading)