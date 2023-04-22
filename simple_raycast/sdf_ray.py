from math import cos, sin
from sdf_Functions import normalize, SignedDistance, offScreen
import variables as _var_


def March(player_pos, angle, objects):
    counter = 0
    dist = 0
    current_position = player_pos
    while counter < 100:
        record = 2000
        for object in objects:
            distance = SignedDistance(current_position, object.position, object.radius)
            if distance < record: record = distance

        if record < 1: break

        x_position = current_position[0] + cos(angle) * record
        y_position = current_position[1] + sin(angle) * record
        a_X = current_position[0] + cos(angle) * record
        a_Y = current_position[1] + sin(angle) * record
        current_position = [normalize(x_position) * a_X,normalize(x_position) * a_Y]
        if offScreen([x_position, y_position], _var_.SCREEN_WIDTH, _var_.SCREEN_HEIGHT): return 2000
        if offScreen(current_position, _var_.SCREEN_WIDTH, _var_.SCREEN_HEIGHT): return 2000
        counter += 1
        dist += record

    return dist
