import math
from simple_raycast.variables import *

def check_collision(player_x, player_y):
    col = int(player_x / TILE_SIZE)
    row = int(player_y / TILE_SIZE)
    index = row * MAP_SIZE + col

    if MAP[index] == wallID:
        if forward == True:
            player_x -= -math.sin(player_angle) * 5
            player_y -= math.cos(player_angle) * 5
        else:
            player_x += -math.sin(player_angle) * 5
            player_y += math.cos(player_angle) * 5

    return player_x,player_y