import pygame as pg
import simple_raycast.variables as _var_

TEXTURE_SIZE = 256
COLUMN_SIZE_X = _var_.SCREEN_WIDTH // _var_.CASTED_RAYS


def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
    texture = pg.image.load(path).convert_alpha()
    return pg.transform.scale(texture, res)


def load_sky_image():
    return get_texture('resources/textures/sky.png', (_var_.SCREEN_WIDTH, _var_.SCREEN_WIDTH // 2))


def load_wall_textures():
    return get_texture('resources/textures/2.png')


wall_tx = load_wall_textures()


def extract_texture_part(offset):
    return wall_tx.subsurface(
        offset * COLUMN_SIZE_X,
        0,
        COLUMN_SIZE_X,
        TEXTURE_SIZE
    )
