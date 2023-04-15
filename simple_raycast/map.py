import simple_raycast.variables as _var_

wallID = "#"
MAP_SIZE = _var_.MAP_SIZE
MAX_INDEX = MAP_SIZE * MAP_SIZE

MAP = (
    '########'
    '#   ## #'
    '#      #'
    '#    ###'
    '##     #'
    '#   #  #'
    '#   #  #'
    '########'
)


# Получаем координаты в 2Д карте(индексы)
def get_coordinates(pos_x, pos_y):
    col = pos_x // _var_.TILE_SIZE
    row = pos_y // _var_.TILE_SIZE
    return col, row


def is_wall(col, row):
    col = int(col)
    row = int(row)
    index = row * _var_.MAP_SIZE + col
    if index > MAX_INDEX - 1 or index < 0:
        return False
    else:
        return MAP[index] == wallID
