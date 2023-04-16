import pygame
import math
import simple_raycast.variables as _var_
import simple_raycast.color as _color_
import numpy as np
import simple_raycast.txloader as txloader

sky_image = txloader.load_sky_image()


def multiply_with_color_depth(image, shading):
    color = (255 / shading) / 255
    if color >= 0.95:
        return image

    imgdata = pygame.surfarray.array3d(image)
    return pygame.surfarray.make_surface(imgdata * color)


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
    draw_solid_floor()

    if _var_.DRAW_SKY:
        draw_sky_image(player_angle)
    else:
        draw_solid_sky()


def get_fixed_fisheye_depth(depth, angle):
    return depth * math.cos(_var_.player_angle - angle)


def get_wall_sector_height(depth, angle):
    depth = get_fixed_fisheye_depth(depth, angle)
    depth = max(depth, 0.0001)  # защита от zero div
    return min(int(_var_.WALL_HEIGHT_PROJ_COEF / depth),
               _var_.SCREEN_HEIGHT)  # защита от гигантского значения высоты стены


def get_wall_segment(ray, depth, angle):
    height = get_wall_sector_height(depth, angle)
    screen_pos_x = ray * _var_.WALL_SECTOR_PX;
    screen_pos_Y = height / 2;
    return np.array([screen_pos_x, screen_pos_Y, _var_.WALL_SECTOR_PX, height])


def get_screen_rect(ray, depth, angle):
    rect = get_wall_segment(ray, depth, angle)

    shift_x = _var_.SCREEN_START[0] + rect[0]
    shift_y = _var_.SCREEN_START[1] - rect[1]
    return np.array([shift_x, shift_y, rect[2], rect[3]])


def draw_reflection(rect, shading):
    rect_reflected = np.array(rect)
    rect_reflected[1] = rect_reflected[1] + rect_reflected[3]
    shape_surf = pygame.Surface(pygame.Rect(rect_reflected).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, _color_.get_color_with_shading(_color_.color_reflection, shading),
                     shape_surf.get_rect())
    _var_.win.blit(shape_surf, rect_reflected)


def draw_wall_solid_color(rect, shading):
    color = _color_.get_color_with_shading(_color_.wall_color, shading)
    pygame.draw.rect(_var_.win, color, rect)


def draw_floor_ao(rect, shading):
    rect_small = np.array(rect)
    rect_small[1] = rect_small[1] + rect_small[3]
    rect_small[3] = (_var_.SCREEN_HEIGHT / 96) / shading;
    rect_small[1] = rect_small[1] - rect_small[3] / 2

    shape_surf = pygame.Surface(pygame.Rect(rect_small).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, _color_.get_color_with_shading(_color_.blackA, shading),
                     shape_surf.get_rect())
    _var_.win.blit(shape_surf, rect_small)


def draw_wall_ao(rect, shading):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, _color_.get_color_with_shading(_color_.blackA, shading),
                     shape_surf.get_rect())
    _var_.win.blit(shape_surf, rect)


def draw_wall_tx(rect, wallId, offset, shading):
    wall_column = txloader.extract_texture_part(wallId, offset)
    wall_column = pygame.transform.scale(wall_column, (rect[2], rect[3]))
    wall_column = wall_column if not _var_.SHADE_TEXTURE else multiply_with_color_depth(wall_column, shading)
    _var_.win.blit(wall_column, (rect[0], rect[1]))


def draw_3D_wall_segment(ray, depth, angle, wallId, offset, is_ao):
    screen_rect = get_screen_rect(ray, depth, angle)
    shading = _color_.get_shading(depth)

    if _var_.DRAW_TEXTURE:
        draw_wall_tx(screen_rect, wallId, offset, shading)
    else:
        draw_wall_solid_color(screen_rect, shading)

    if _var_.DRAW_REFLECTION:
        draw_reflection(screen_rect, shading)

    if _var_.DRAW_AO:
        if shading > 1.5: return
        # draw_floor_ao(screen_rect, shading)
        if is_ao:
            draw_wall_ao(screen_rect, shading)
