import pygame as pg
from settings import *


def get_color_by_depth(depth):
    return [255 / (1 + depth ** 5 * .00002)] * 3


class Render:
    def __init__(self, game):
        self.game = game

    def draw(self):
        if self.game.render_type == RenderType.TwoD:
            self.draw_2d()
        elif self.game.render_type == RenderType.Walls:
            self.draw_walls()
        elif self.game.render_type == RenderType.WallsTextures:
            self.draw_walls_textures()

    def draw_2d(self):
        self.game.screen.fill(COLOR_WINDOW_BACK)
        self.game.map_view.draw()
        self.game.player_view.render()

    def draw_walls(self):
        self.game.object_renderer.draw()

    def draw_walls_textures(self):
        self.game.object_renderer.draw()

    def render_raycast(self, x, y, depth, sin_a, cos_a, ray, proj_height):
        if self.game.render_type == RenderType.TwoD:
            start_x, start_y = CELL_SIZE * x, CELL_SIZE * y
            width = CELL_SIZE * depth
            self.game.ray_view.draw(start_x, start_y, width, sin_a, cos_a, COLOR_RAY)
            pass
        elif self.game.render_type == RenderType.Walls:
            if self.game.render_type == RenderType.Walls:
                color = get_color_by_depth(depth)
                pg.draw.rect(self.game.screen, color, (ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height))
        elif self.game.render_type == RenderType.WallsTextures:
            pass
