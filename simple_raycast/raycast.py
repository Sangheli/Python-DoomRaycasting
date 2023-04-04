import math
import simple_raycast.render2D as render2D
import simple_raycast.render3D as render3D
import simple_raycast.variables as _var_


# Получаем проекции треугольника(x,y), исходя из угла и длины гипотенузы(angle,depth)
def get_ray_projection(player_x, player_y, angle, depth):
    ray_x = player_x - math.sin(angle) * depth
    ray_y = player_y + math.cos(angle) * depth
    return ray_x, ray_y


# Получаем координаты в 2Д карте(индексы)
def get_cell_coordinates(ray_x, ray_y):
    col = int(ray_x / _var_.TILE_SIZE)
    row = int(ray_y / _var_.TILE_SIZE)
    return col, row


def get_map_cell_index(col, row):
    return row * _var_.MAP_SIZE + col


def cast_rays(player_x, player_y):
    start_angle = _var_.player_angle - _var_.HALF_FOV

    for ray in range(_var_.CASTED_RAYS):
        angle = start_angle + ray * _var_.STEP_ANGLE
        for depth in range(_var_.MAX_DEPTH):
            ray_x, ray_y = get_ray_projection(player_x, player_y, angle, depth)
            col, row = get_cell_coordinates(ray_x, ray_y)
            index = get_map_cell_index(col, row)
            if _var_.MAP[index] == _var_.wallID:
                render2D.draw_2D_rays(col, row, ray_x, ray_y, player_x, player_y)
                render3D.draw_3D_wall_segment(ray, depth, angle)
                break
