import pygame as pg
import simple_raycast.variables as _var_

TEXTURE_SIZE = 256


def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
    texture = pg.image.load(path).convert_alpha()
    return pg.transform.scale(texture, res)


def load_sky_image():
    return get_texture('resources/textures/sky.png', (_var_.SCREEN_WIDTH, _var_.SCREEN_WIDTH//2))
