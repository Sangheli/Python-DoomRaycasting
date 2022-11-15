import pygame as pg
from settings import *


def multiply_with_color_depth(image, depth, horizontal):
    color = (255 / (1 + depth ** 5 * .00002)) / 255
    if color >= 0.95:
        return image

    imgdata = pg.surfarray.array3d(image)
    return pg.surfarray.make_surface(imgdata * color)


class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.game.textureloader.load_wall_textures()
        self.sky_image = self.game.textureloader.load_sky_image()
        self.sky_offset = 0

    def draw(self):
        self.draw_background()
        self.draw_floor()
        self.render_game_objects()

    def draw_background(self):
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))

    def draw_floor(self):
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        list_objects = self.game.raycasting.objects_to_render
        for depth, image, screen_pos,horizontal in list_objects:
            image = multiply_with_color_depth(image, depth, horizontal)
            self.screen.blit(image, screen_pos)
