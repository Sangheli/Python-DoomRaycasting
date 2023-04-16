import pygame as pg
import simple_raycast.variables as _var_

TEXTURE_SIZE = 256
COLUMN_SIZE_X = 480 // _var_.CASTED_RAYS


def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
    texture = pg.image.load(path).convert_alpha()
    return pg.transform.scale(texture, res)


def load_sky_image():
    return get_texture('resources/textures/sky.png', (_var_.SCREEN_WIDTH, _var_.SCREEN_WIDTH // 2))


def load_wall_textures():
    return {
            '1':get_texture('resources/textures/1.png'),
            '2':get_texture('resources/textures/2.png'),
            '3':get_texture('resources/textures/3.png'),
            '4':get_texture('resources/textures/4.png'),
            '5':get_texture('resources/textures/5.png'),
    }


wall_tx = load_wall_textures()


def extract_texture_part(wallId, offset):
    return wall_tx[wallId].subsurface(
        offset * COLUMN_SIZE_X,
        0,
        COLUMN_SIZE_X,
        TEXTURE_SIZE
    )
