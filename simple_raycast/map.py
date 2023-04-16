import simple_raycast.variables as _var_

wallID = "#"
MAP_SIZE = _var_.MAP_SIZE
MAX_INDEX = MAP_SIZE * MAP_SIZE
world_map = {}

MAP = (
    '12121212',
    '1     21',
    '15   3 1',
    '1 4    1',
    '2      1',
    '1  23422',
    '1      1',
    '12212121'
)

for j, row in enumerate(MAP):
    for i, char in enumerate(row):
        if char != ' ':
            world_map[(i, j)] = char


# Получаем координаты в 2Д карте(индексы)
def get_coordinates(pos_x, pos_y):
    col = pos_x // _var_.TILE_SIZE
    row = pos_y // _var_.TILE_SIZE
    return col, row


def is_wall(tile):
    return tile in world_map
