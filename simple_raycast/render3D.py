import pygame
import math
import simple_raycast.variables as _var_
import simple_raycast.color as _color_
import numpy as np


def draw_3D_back():
    pygame.draw.rect(_var_.win, _color_.backGround,
                     (_var_.SHIFT_WIDTH, _var_.SCREEN_HEIGHT / 2, _var_.SCREEN_HEIGHT, _var_.SCREEN_HEIGHT))
    pygame.draw.rect(_var_.win, _color_.backSky,
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


def get_wall_segment(ray, depth, angle):
    height = get_wall_sector_height(depth, angle)
    screen_pos_x = ray * _var_.WALL_SECTOR_SIZE_PX;
    screen_pos_Y = height / 2;
    return np.array([screen_pos_x, screen_pos_Y, _var_.WALL_SECTOR_SIZE_PX, height])


def draw_reflection(rect, depth):
    rect[1] = rect[1] + rect[3]
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, get_shading(_color_.color_reflection, depth), shape_surf.get_rect())
    _var_.win.blit(shape_surf, rect)


def draw_normal(color, new_rect):
    shift_x = _var_.screen_shift[0] + new_rect[0]
    shift_y = _var_.screen_shift[1] - new_rect[1]
    new_rect = np.array([shift_x, shift_y, new_rect[2], new_rect[3]])
    pygame.draw.rect(_var_.win, color, new_rect)
    return new_rect


def draw_3D_wall_segment(ray, depth, angle):
    color = get_shading(_color_.wall_color, depth)
    rect  = get_wall_segment(ray, depth, angle)
    world_rect = draw_normal(color, rect)
    draw_reflection(world_rect, depth)
