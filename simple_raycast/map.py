import simple_raycast.variables as _var_

wallID = "#"
MAP_SIZE = _var_.MAP_SIZE

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
    col = int(pos_x / _var_.TILE_SIZE)
    row = int(pos_y / _var_.TILE_SIZE)
    return col, row


def is_wall(col, row):
    index = row * _var_.MAP_SIZE + col
    return MAP[index] == wallID
