import pygame
import math
import variables as _var_
import color as _color_
import numpy as np
import txloader as txloader
from numba import njit

sky_image = txloader.load_sky_image()

floor_tx_size = 100
floor_scale_size = 300
floor_frame = np.random.uniform(0, 1, (floor_scale_size, floor_scale_size, 3))

floo_base_image = txloader.load_floor(floor_tx_size)
floo_base_image = pygame.transform.rotate(floo_base_image, 90)
floor_image = pygame.surfarray.array3d(floo_base_image) / 255
floor_angle_mod = floor_scale_size / np.rad2deg(_var_.FOV)

sky_surf = pygame.Surface((_var_.SCREEN_WIDTH, _var_.HALF_HEIGHT))

def multiply_with_color_depth(image, shading):
    color = (255 / shading) / 255
    if color >= 0.95:
        return image

    imgdata = pygame.surfarray.array3d(image)
    return pygame.surfarray.make_surface(imgdata * color)


def draw_solid_sky(frame):
    pygame.draw.rect(frame, _color_.backSky,
                     (_var_.SCREEN_START[0], -_var_.SCREEN_START[1], _var_.SCREEN_WIDTH, _var_.SCREEN_HEIGHT))


def draw_sky_image(frame, player_angle):
    sky_offset = (50 * player_angle) % _var_.SCREEN_WIDTH
    frame.blit(sky_image, (_var_.SCREEN_START[0] - sky_offset, 0))
    frame.blit(sky_image, (_var_.SCREEN_START[0] - sky_offset + _var_.SCREEN_WIDTH, 0))


def draw_solid_floor(frame):
    pygame.draw.rect(frame, _color_.backGround,
                     (_var_.SCREEN_START[0], _var_.SCREEN_START[1], _var_.SCREEN_WIDTH, _var_.SCREEN_HEIGHT))


def draw_textured_floor(main_frame,sky_surf, player_x, player_y):
    frame = get_floor_frame(player_x / _var_.TILE_SIZE, player_y / _var_.TILE_SIZE, _var_.player_angle, floor_frame,
                            floor_image, floor_scale_size, floor_scale_size, floor_angle_mod)

    floor_surf = pygame.surfarray.make_surface(frame * 255)
    floor_surf = pygame.transform.scale(floor_surf, (_var_.SCREEN_WIDTH, _var_.HALF_HEIGHT))
    if not _var_.DRAW_REFLECTION or not _var_.DRAW_FLOOR_SKY_REFLECTION:
        main_frame.blit(floor_surf, _var_.SCREEN_START)
        return

    sky_surf.blit(main_frame, (_var_.SCREEN_START[0], 0,_var_.SCREEN_WIDTH, _var_.HALF_HEIGHT))
    sky_surf = pygame.transform.flip(sky_surf, False, True)

    reflected_image = 0.75 * pygame.surfarray.array3d(floor_surf) + 0.25 * pygame.surfarray.array3d(sky_surf)
    reflected_surf = pygame.surfarray.make_surface(reflected_image)

    main_frame.blit(reflected_surf, _var_.SCREEN_START)


@njit()
def get_floor_frame(posx, posy, player_angle, frame, floor_image, width, height, angle_mod):
    for col in range(width):
        angle_shift = np.deg2rad(col / angle_mod - 30)
        angle = player_angle + angle_shift
        sin_a, cos_a, cos_a_shift = np.sin(angle), np.cos(angle), np.cos(angle_shift)
        for row in range(height):
            depth = (height / (height - row)) / cos_a_shift
            x, y = posx + cos_a * depth, posy + sin_a * depth
            xx, yy = int(x * 3 % 1 * 100), int(y * 3 % 1 * 100)
            frame[col][-row] = floor_image[xx][yy]

    return frame


def draw_3D_back(frame, player_angle, player_x, player_y):
    if _var_.DRAW_TEXTURE and _var_.DRAW_FLOOR_TX:
        draw_textured_floor(frame,sky_surf, player_x, player_y)
    else:
        draw_solid_floor(frame)

    if _var_.DRAW_TEXTURE and _var_.DRAW_SKY:
        draw_sky_image(frame, player_angle)
    else:
        draw_solid_sky(frame)


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


def draw_reflection(frame, rect, shading):
    rect_reflected = np.array(rect)
    rect_reflected[1] = rect_reflected[1] + rect_reflected[3]
    shape_surf = pygame.Surface(pygame.Rect(rect_reflected).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, _color_.get_color_with_shading(_color_.color_reflection, shading),
                     shape_surf.get_rect())
    frame.blit(shape_surf, rect_reflected)


def draw_wall_solid_color(frame, rect, shading):
    color = _color_.get_color_with_shading(_color_.wall_color, shading)
    pygame.draw.rect(frame, color, rect)


def draw_wall_tx(frame, rect, wallId, offset, shading, proj_height):
    isTiny = proj_height < _var_.SCREEN_HEIGHT

    wall_column = txloader.extract_texture_part(wallId, offset, proj_height)
    wall_column = pygame.transform.scale(wall_column, (rect[2], proj_height if isTiny else _var_.SCREEN_HEIGHT))
    wall_column = wall_column if not _var_.SHADE_TEXTURE else multiply_with_color_depth(wall_column, shading)

    wall_pos_y = _var_.HALF_HEIGHT - proj_height // 2 if isTiny else 0
    wall_pos = (rect[0], wall_pos_y)
    frame.blit(wall_column, wall_pos)


def draw_3D_wall_segment(frame, ray, depth, angle, wallId, offset):
    proj_height = _var_.SCREEN_DIST / (
            get_fixed_fisheye_depth(depth / _var_.TILE_SIZE, _var_.player_angle, angle) + 0.0001)

    screen_rect = get_screen_rect(ray, proj_height)
    shading = _color_.get_shading(depth)

    if _var_.DRAW_TEXTURE:
        draw_wall_tx(frame, screen_rect, wallId, offset, shading, proj_height)
    else:
        draw_wall_solid_color(frame,screen_rect, shading)

    if _var_.DRAW_REFLECTION:
        draw_reflection(frame, screen_rect, shading)
