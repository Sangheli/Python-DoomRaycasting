import pygame as pg
import simple_raycast.variables as _var_

TEXTURE_SIZE = 256
COLUMN_SIZE_X = _var_.SCREEN_WIDTH // _var_.CASTED_RAYS
HALF_TX_SIZE = TEXTURE_SIZE // 2


def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
    texture = pg.image.load(path).convert_alpha()
    return pg.transform.scale(texture, res)


def load_sky_image():
    return get_texture('resources/textures/sky.png', (_var_.SCREEN_WIDTH, _var_.SCREEN_WIDTH // 2))


def load_floor():
    return get_texture('resources/textures/floor.jpg', (100, 100))


def load_wall_textures():
    return {
        1: get_texture('resources/textures/1.png'),
        2: get_texture('resources/textures/2.png'),
        3: get_texture('resources/textures/3.png'),
        4: get_texture('resources/textures/4.png'),
        5: get_texture('resources/textures/5.png'),
    }


wall_tx = load_wall_textures()


def extract_texture_part(wallId, offset, proj_height):
    if proj_height < _var_.SCREEN_HEIGHT:
        return wall_tx[wallId].subsurface(
            offset * (TEXTURE_SIZE - COLUMN_SIZE_X), 0, COLUMN_SIZE_X, TEXTURE_SIZE
        )
    else:
        height = TEXTURE_SIZE * _var_.SCREEN_HEIGHT / proj_height
        return wall_tx[wallId].subsurface(
            offset * (TEXTURE_SIZE - COLUMN_SIZE_X), HALF_TX_SIZE - height // 2, COLUMN_SIZE_X, height
        )
