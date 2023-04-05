import pygame as pg
import simple_raycast.variables as _var_

TEXTURE_SIZE = 256


def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
    texture = pg.image.load(path).convert_alpha()
    return pg.transform.scale(texture, res)
