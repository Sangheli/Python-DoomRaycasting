import math
import simple_raycast.render2D as render2D
import simple_raycast.render3D as render3D
import simple_raycast.variables as _var_


def cast_rays(player_x, player_y):
    start_angle = _var_.player_angle - _var_.HALF_FOV

    for ray in range(_var_.CASTED_RAYS):
        for depth in range(_var_.MAX_DEPTH):
            target_x = player_x - math.sin(start_angle) * depth
            target_y = player_y + math.cos(start_angle) * depth
            col = int(target_x / _var_.TILE_SIZE)
            row = int(target_y / _var_.TILE_SIZE)
            index = row * _var_.MAP_SIZE + col

            if _var_.MAP[index] == _var_.wallID:
                render2D.draw_2D_rays(col, row, target_x, target_y, player_x, player_y)
                render3D.draw_3D_wall_segment(ray, depth, start_angle)
                break

        start_angle += _var_.STEP_ANGLE
