import math
import simple_raycast.render2D as render2D
import simple_raycast.render3D as render3D
import simple_raycast.variables as _var_
import simple_raycast.map as map
import pygame

def print_raycount(count):
    text = 'rays: '+str(count)
    font = pygame.font.SysFont('Monospace Regular', 30)
    textsurface = font.render(text, False, (255, 255, 255))
    _var_.win.blit(textsurface, (80, 0))

def print_pos(x,y):
    text = '('+str(int(x))+','+str(int(y))+')'
    font = pygame.font.SysFont('Monospace Regular', 30)
    textsurface = font.render(text, False, (255, 255, 255))
    _var_.win.blit(textsurface, (30, 0))

# Получаем проекции треугольника(x,y), исходя из угла и длины гипотенузы(angle,depth)
def get_ray_projection(player_x, player_y, _sin,_cos, depth):
    ray_x = player_x - _sin * depth
    ray_y = player_y + _cos * depth
    return ray_x, ray_y


# TODO оптизировать бросок лучей, сначала по поиску ячеек сетки, а уже потом искать длину луча
def cast_rays(player_x, player_y):
    cast_rays_new(player_x,player_y)
    return

    count = 0
    start_angle = _var_.player_angle - _var_.HALF_FOV

    for ray_index in range(_var_.CASTED_RAYS):
        angle = start_angle + ray_index * _var_.STEP_ANGLE
        _sin = math.sin(angle)
        _cos = math.cos(angle)
        # Проверяем луч на каждом из указанных шагов глубины
        for depth in range(0,_var_.MAX_DEPTH):
            count += 1
            ray_x, ray_y = get_ray_projection(player_x, player_y,_sin,_cos, depth)
            col, row = map.get_coordinates(ray_x, ray_y)
            if map.is_wall(col, row):
                render2D.draw_2D_rays(col, row, ray_x, ray_y, player_x, player_y)
                render3D.draw_3D_wall_segment(ray_index, depth, angle)
                break

    print_raycount(count)

def cast_rays_new(player_x, player_y):
    count = 0
    depth_step = 10

    start_angle = _var_.player_angle - _var_.HALF_FOV

    for ray_index in range(_var_.CASTED_RAYS):
        big_count = 0
        angle = start_angle + ray_index * _var_.STEP_ANGLE
        _sin = math.sin(angle)
        _cos = math.cos(angle)
        # Проверяем луч на каждом из указанных шагов глубины
        for depth in range(0,_var_.MAX_DEPTH,depth_step):
            big_count+=1
            ray_x, ray_y = get_ray_projection(player_x, player_y,_sin,_cos, depth)
            col, row = map.get_coordinates(ray_x, ray_y)
            if map.is_wall(col, row):
                count += big_count - 1 + cast_subrays(player_x, player_y, _sin, _cos, ray_index, angle, depth - depth_step)
                break

    print_raycount(count)

def cast_subrays(player_x, player_y, _sin, _cos, ray_index, angle, start):
    subCount = 0
    for depth in range(start, _var_.MAX_DEPTH,1):
        subCount+=1
        ray_x, ray_y = get_ray_projection(player_x, player_y, _sin, _cos, depth)
        col, row = map.get_coordinates(ray_x, ray_y)
        # Проверяем луч на каждом из указанных шагов глубины
        if map.is_wall(col, row):
            render2D.draw_2D_rays(col, row, ray_x, ray_y, player_x, player_y)
            render3D.draw_3D_wall_segment(ray_index, depth, angle)
            return subCount

    return 0
