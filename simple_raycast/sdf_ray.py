from math import cos, sin
from sdf_Functions import normalize, SignedDistance, offScreen
import variables as _var_


def March(player_pos, angle, objects):
    counter = 0
    dist = 0
    pos = player_pos
    while counter < 100:
        record, current = find_nearest(pos, objects)
        if record < 1: break
        x_p, y_p = pos[0] + cos(angle) * record, pos[1] + sin(angle) * record
        a_X, a_Y = pos[0] + cos(angle) * record, pos[1] + sin(angle) * record
        pos = [normalize(x_p) * a_X, normalize(x_p) * a_Y]
        if offScreen([x_p, y_p], _var_.SCREEN_WIDTH, _var_.SCREEN_HEIGHT): return 1000, None
        if offScreen(pos, _var_.SCREEN_WIDTH, _var_.SCREEN_HEIGHT): return 1000, None
        counter += 1
        dist += record

    return dist, current


def find_nearest(pos, objects):
    current = None
    record = 1000
    for obj in objects:
        distance = SignedDistance(pos, obj.position, obj.radius)
        if distance < record:
            record = distance
            current = obj

    return record, current
