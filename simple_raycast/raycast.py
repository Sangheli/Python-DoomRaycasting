import math
import simple_raycast.render2D as render2D
import simple_raycast.render3D as render3D
import simple_raycast.variables as _var_
import simple_raycast.map as map


# Получаем проекции треугольника(x,y), исходя из угла и длины гипотенузы(angle,depth)
def get_ray_projection(player_x, player_y, angle, depth):
    ray_x = player_x - math.sin(angle) * depth
    ray_y = player_y + math.cos(angle) * depth
    return ray_x, ray_y


def cast_rays(player_x, player_y):
    start_angle = _var_.player_angle - _var_.HALF_FOV

    for ray in range(_var_.CASTED_RAYS):
        angle = start_angle + ray * _var_.STEP_ANGLE
        # Проверяем луч на каждом из указанных шагов глубины
        for depth in range(0,_var_.MAX_DEPTH,2):
            ray_x, ray_y = get_ray_projection(player_x, player_y, angle, depth)
            col, row = map.get_coordinates(ray_x, ray_y)
            if map.is_wall(col, row):
                render2D.draw_2D_rays(col, row, ray_x, ray_y, player_x, player_y)
                render3D.draw_3D_wall_segment(ray, depth, angle)
                break
