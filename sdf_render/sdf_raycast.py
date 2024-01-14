import sdf_render3D as render3D
from simple_raycast import variables as _var_
import sdf_ray as ray
import sdf_render2D as render2D

def smin(a,b,k):
    h = max(k-abs(a-b),0.)/k
    return min(a,b)-h*h*h*k*(1./6.)

def cast_rays(player_x, player_y, frame, objects,objectsSq):
    casted_walls = ray_casting(player_x, player_y,_var_.player_angle, objects,objectsSq)

    for ray_index, depth, angle,obj in casted_walls:
        if obj is None:
            continue

        render2D.draw_ray(frame, player_x, player_y, depth,angle)
        render3D.draw_3D_wall_segment(frame, ray_index, depth, angle,obj)


def ray_casting(player_x, player_y, player_angle, objects,objectsSq):
    casted_walls = []
    start_angle = player_angle - _var_.HALF_FOV
    for ray_index in range(_var_.CASTED_RAYS):
        angle = start_angle + ray_index * _var_.STEP_ANGLE
        depth1,obj1 = ray.March([player_x, player_y], angle, objects)
        depth2,obj2 = ray.March([player_x, player_y], angle, objectsSq)

        if obj1 is not None and obj2 is not None:
            depth = smin(depth1,depth2,20.0)
            depth = max(depth1,-depth2)
            depth = max(depth2,-depth2)
            # depth = max(depth2,depth1)

            if(ray_index==240):
                print(depth)
            obj = obj1

        if obj1 is None and obj2 is not None:
            depth = depth2
            obj = obj2

        if obj2 is None and obj1 is not None:
            depth = depth1
            obj = obj1

        if obj1 is None and obj2 is None:
            continue

        casted_walls.append((ray_index,depth, angle,obj))

    return casted_walls
