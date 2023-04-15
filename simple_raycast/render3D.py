import pygame
import math
import simple_raycast.variables as _var_
import simple_raycast.color as _color_
import numpy as np
import simple_raycast.txloader as txloader

sky_image = txloader.load_sky_image()


def draw_solid_sky():
    pygame.draw.rect(_var_.win, _color_.backSky,
                     (_var_.SCREEN_START[0], -_var_.SCREEN_START[1], _var_.SCREEN_WIDTH, _var_.SCREEN_HEIGHT))


def draw_sky_image(angle_rel):
    sky_offset = (50 * angle_rel) % _var_.SCREEN_WIDTH
    _var_.win.blit(sky_image, (_var_.SCREEN_START[0] - sky_offset, 0))
    _var_.win.blit(sky_image, (_var_.SCREEN_START[0] - sky_offset + _var_.SCREEN_WIDTH, 0))


def draw_solid_floor():
    pygame.draw.rect(_var_.win, _color_.backGround,
                     (_var_.SCREEN_START[0], _var_.SCREEN_START[1], _var_.SCREEN_WIDTH, _var_.SCREEN_HEIGHT))


def draw_3D_back(player_angle):
    draw_sky_image(player_angle)
    draw_solid_floor()
    # draw_solid_sky()


def get_shading(color, depth):
    return np.array(color) / (1 + depth * depth * 0.0001)


def get_fixed_fisheye_depth(depth, angle):
    return depth * math.cos(_var_.player_angle - angle)


def get_wall_sector_height(depth, angle):
    depth = get_fixed_fisheye_depth(depth, angle)
    depth = max(depth, 0.0001)  # защита от zero div
    return min(int(_var_.WALL_HEIGHT_BASE / depth), _var_.SCREEN_HEIGHT)  # защита от гигантского значения высоты стены


def get_wall_segment(ray, depth, angle):
    height = get_wall_sector_height(depth, angle)
    screen_pos_x = ray * _var_.WALL_SECTOR_PX;
    screen_pos_Y = height / 2;
    return np.array([screen_pos_x, screen_pos_Y, _var_.WALL_SECTOR_PX, height])


def draw_reflection(rect, depth):
    rect_reflected = np.array(rect)
    rect_reflected[1] = rect_reflected[1] + rect_reflected[3]
    shape_surf = pygame.Surface(pygame.Rect(rect_reflected).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, get_shading(_color_.color_reflection, depth), shape_surf.get_rect())
    _var_.win.blit(shape_surf, rect_reflected)


def get_world_rect(rect):
    shift_x = _var_.SCREEN_START[0] + rect[0]
    shift_y = _var_.SCREEN_START[1] - rect[1]
    return np.array([shift_x, shift_y, rect[2], rect[3]])


def draw_wall_solid_color(rect, depth):
    color = get_shading(_color_.wall_color, depth)
    pygame.draw.rect(_var_.win, color, rect)


def draw_3D_wall_segment(ray, depth, angle):
    rect = get_wall_segment(ray, depth, angle)
    world_rect = get_world_rect(rect)

    draw_wall_solid_color(world_rect, depth)
    draw_reflection(world_rect, depth)
