import math
import simple_raycast.map as map


def check_collision(player_x, player_y, player_angle, forward):
    col, row = map.get_coordinates(player_x, player_y)
    if map.is_wall(col, row):
        if forward:
            player_x -= -math.sin(player_angle) * 5
            player_y -= math.cos(player_angle) * 5
        else:
            player_x += -math.sin(player_angle) * 5
            player_y += math.cos(player_angle) * 5

    return player_x, player_y
