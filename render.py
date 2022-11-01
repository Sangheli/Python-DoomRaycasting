import numpy as np
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
            np_start = np.array((x,y)) * CELL_SIZE
            depth_full = CELL_SIZE * depth
            self.game.ray_view.draw(np_start, depth_full, sin_a, cos_a, COLOR_RAY, (MAP_SHIFT_X, MAP_SHIFT_Y))
            pass
        elif self.game.render_type == RenderType.Walls:
            if self.game.render_type == RenderType.Walls:
                color = get_color_by_depth(depth)
                rect = (ray * COLUMN_SIZE_X, HALF_HEIGHT - proj_height // 2, COLUMN_SIZE_X, proj_height)
                pg.draw.rect(self.game.screen, color, rect)
        elif self.game.render_type == RenderType.WallsTextures:
            pass
