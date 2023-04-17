import math
from numba import njit
from numba import int32

import simple_raycast.render2D as render2D
import simple_raycast.render3D as render3D
import simple_raycast.variables as _var_
import simple_raycast.map as map
import pygame

WIDTH = _var_.MAP_SIZE * _var_.TILE_SIZE
HEIGHT = _var_.MAP_SIZE * _var_.TILE_SIZE

def print_raycount(count):
    text = 'rays: ' + str(count)
    font = pygame.font.SysFont('Monospace Regular', 30)
    textsurface = font.render(text, False, (255, 255, 255))
    _var_.win.blit(textsurface, (120, 0))


def print_pos(x, y):
    text = '(' + str(int(x)) + ',' + str(int(y)) + ')'
    font = pygame.font.SysFont('Monospace Regular', 30)
    textsurface = font.render(text, False, (255, 255, 255))
    _var_.win.blit(textsurface, (30, 0))


@njit(fastmath=True)
def mapping(a, b):
    return (a // _var_.TILE_SIZE) * _var_.TILE_SIZE, (b // _var_.TILE_SIZE) * _var_.TILE_SIZE


@njit(fastmath=True)
def map_get_coordinates(a, b):
    return a // _var_.TILE_SIZE, b // _var_.TILE_SIZE

@njit(fastmath=True)
def get_sin_cos(angle):
    sin_a = math.sin(angle)
    cos_a = math.cos(angle)
    return sin_a if sin_a else 0.000001, cos_a if cos_a else 0.000001


@njit(fastmath=True)
def get_data_vert(ox, oy, xm, ym, sin_a, cos_a, WIDTH, world_map):
    subCount = 0
    x, dx = (xm + _var_.TILE_SIZE, 1) if cos_a >= 0 else (xm, -1)
    # Проход по каждому из вертикальных столбцов
    for i in range(0, WIDTH, _var_.TILE_SIZE):
        subCount += 1
        depth_v = (x - ox) / cos_a
        y = oy + depth_v * sin_a
        tile = map_get_coordinates(x + dx, y)
        is_wall = tile in world_map
        if is_wall: return x, y, depth_v, subCount, world_map[tile]
        x += dx * _var_.TILE_SIZE

    return x, y, depth_v, subCount, 0


@njit(fastmath=True)
def get_data_hori(ox, oy, xm, ym, sin_a, cos_a, HEIGHT, world_map):
    subCount = 0
    y, dy = (ym + _var_.TILE_SIZE, 1) if sin_a >= 0 else (ym, -1)
    # Проход по каждой из горзионтальных строк
    for i in range(0, HEIGHT, _var_.TILE_SIZE):
        subCount += 1
        depth_h = (y - oy) / sin_a
        x = ox + depth_h * cos_a
        tile = map_get_coordinates(x, y + dy)
        is_wall = tile in world_map
        if is_wall: return x, y, depth_h, subCount, world_map[tile]
        y += dy * _var_.TILE_SIZE

    return x, y, depth_h, subCount, 0


def cast_rays(player_x, player_y):
    casted_walls, count = ray_casting(player_x, player_y,_var_.player_angle, map.world_map)
    print_raycount(count)

    for ray_index, depth, angle, wallId, offset, x, y, isAo in casted_walls:
        render2D.draw_ray(player_x, player_y, x, y)
        render3D.draw_3D_wall_segment(ray_index, depth, angle, wallId, offset, False)


@njit(fastmath=True)
def ray_casting(player_x, player_y,player_angle, world_map):
    casted_walls = []
    count = 0
    xm, ym = mapping(player_x, player_y)
    start_angle = player_angle - _var_.HALF_FOV
    prev_vert = False
    for ray_index in range(_var_.CASTED_RAYS):
        angle = start_angle + ray_index * _var_.STEP_ANGLE
        sin_a, cos_a = get_sin_cos(angle)

        x1, y1, depth_v, subCount1, tx1 = get_data_vert(player_x, player_y, xm, ym, sin_a, cos_a, WIDTH, world_map)
        x2, y2, depth_h, subCount2, tx2 = get_data_hori(player_x, player_y, xm, ym, sin_a, cos_a, HEIGHT, world_map)
        isVert = depth_v < depth_h

        x,y,depth,wallId = (x1,y1,depth_v,tx1) if isVert else (x2,y2,depth_h,tx2)
        if wallId == 0: continue
        offset = (y1 if isVert else x2) / _var_.TILE_SIZE % 1
        if isVert: offset = offset if cos_a > 0 else (1 - offset)
        else: offset = (1 - offset) if sin_a > 0 else offset
        if ray_index == 0: prev_vert = isVert

        casted_walls.append((ray_index, depth, angle, wallId, offset, x, y, prev_vert != isVert))
        prev_vert = isVert
        count += subCount1 + subCount2

    return casted_walls, count
