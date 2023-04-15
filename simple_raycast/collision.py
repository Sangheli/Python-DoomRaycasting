import math
import simple_raycast.map as map
import simple_raycast.variables as _var_

def check_collision(player_x, player_y, player_angle, forward,DELTATIME):
    col, row = map.get_coordinates(player_x, player_y)
    if map.is_wall(col, row):
        if forward:
            player_x -= math.cos(player_angle) * _var_.PLAYER_SPEED * DELTATIME
            player_y -= math.sin(player_angle) * _var_.PLAYER_SPEED * DELTATIME
        else:
            player_x += math.cos(player_angle) * _var_.PLAYER_SPEED * DELTATIME
            player_y += math.sin(player_angle) * _var_.PLAYER_SPEED * DELTATIME

    return player_x, player_y
