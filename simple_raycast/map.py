import variables as _var_
from numba.core import types
from numba.typed import Dict
from numba import int32, int64, njit

MAP_SIZE = _var_.MAP_SIZE
world_map = Dict.empty(key_type=types.UniTuple(int32, 2), value_type=int32)

_ = False
MAP = [
    [1, 1, 1, 1, 1, 2, 1, 1],
    [1, _, _, _, _, _, 2, 1],
    [1, 5, _, _, _, 3, _, 1],
    [1, _, 4, _, _, _, _, 1],
    [2, _, _, _, _, _, _, 1],
    [1, _, _, 2, 3, 4, 2, 2],
    [1, _, _, _, _, _, _, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
]

for j, row in enumerate(MAP):
    for i, char in enumerate(row):
        if char != _: world_map[(int32(i), int32(j))] = char


# Получаем координаты в 2Д карте(индексы)
def get_coordinates(pos_x, pos_y):
    col = pos_x // _var_.TILE_SIZE
    row = pos_y // _var_.TILE_SIZE
    return col, row


def is_wall(tile):
    return tile in world_map
