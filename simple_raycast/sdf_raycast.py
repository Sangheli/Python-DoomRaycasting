import sdf_render3D as render3D
import variables as _var_
import sdf_ray as ray


def cast_rays(player_x, player_y, frame, objects):
    casted_walls = ray_casting(player_x, player_y,_var_.player_angle, objects)

    for ray_index, depth, angle in casted_walls:
        if depth>1000: continue
        render3D.draw_3D_wall_segment(frame, ray_index, depth, angle)


def ray_casting(player_x, player_y, player_angle, objects):
    casted_walls = []
    start_angle = player_angle - _var_.HALF_FOV
    for ray_index in range(_var_.CASTED_RAYS):
        angle = start_angle + ray_index * _var_.STEP_ANGLE
        depth = ray.March([player_x, player_y], angle, objects)
        casted_walls.append((ray_index, depth, angle))

    return casted_walls
