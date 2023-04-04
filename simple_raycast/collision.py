import math
import simple_raycast.variables as _var_

def check_collision(player_x, player_y,player_angle,forward):
    col = int(player_x / _var_.TILE_SIZE)
    row = int(player_y / _var_.TILE_SIZE)
    index = row * _var_.MAP_SIZE + col

    if _var_.MAP[index] == _var_.wallID:
        if forward == True:
            player_x -= -math.sin(player_angle) * 5
            player_y -= math.cos(player_angle) * 5
        else:
            player_x += -math.sin(player_angle) * 5
            player_y += math.cos(player_angle) * 5

    return player_x,player_y