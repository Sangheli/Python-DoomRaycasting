import pygame as pg
from settings import *


class PlayerView:
    def __init__(self, game):
        self.game = game

    def render(self):
        self.draw_player(self.game.player.x, self.game.player.y, MAP_SHIFT_X, MAP_SHIFT_Y)
        self.draw_player_ray(self.game.player.x, self.game.player.y, self.game.player.angle, MAP_SHIFT_X, MAP_SHIFT_Y)

    def draw_player(self, x, y,shiftx,shifty):
        pg.draw.circle(self.game.screen, COLOR_PLAYER, (shiftx + x * CELL_SIZE, shifty + y * CELL_SIZE), CELL_SIZE//6)

    def draw_player_ray(self, x, y, angle,shiftx,shifty):
        start_x, start_y = CELL_SIZE * x, CELL_SIZE * y
        sin_a = math.sin(angle)
        cos_a = math.cos(angle)
        self.game.ray_view.draw(start_x, start_y, WIDTH, sin_a, cos_a, COLOR_RAY_RED, shiftx, shifty)
