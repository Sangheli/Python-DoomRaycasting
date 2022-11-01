import numpy as np
import pygame as pg
from settings import *


class PlayerView:
    def __init__(self, game):
        self.game = game

    def render(self):
        self.draw_player((self.game.player.x, self.game.player.y), (MAP_SHIFT_X, MAP_SHIFT_Y))
        self.draw_player_ray((self.game.player.x, self.game.player.y), self.game.player.angle, (MAP_SHIFT_X, MAP_SHIFT_Y))

    def draw_player(self, pos, shift):
        np_pos = np.array(pos)
        np_shift = np.array(shift)
        pg.draw.circle(self.game.screen, COLOR_PLAYER, np_pos * CELL_SIZE + np_shift, CELL_SIZE//6)

    def draw_player_ray(self, pos, angle, shift):
        np_start_pos = np.array(pos) * CELL_SIZE
        sin_a = math.sin(angle)
        cos_a = math.cos(angle)
        self.game.ray_view.draw(np_start_pos, WIDTH, sin_a, cos_a, COLOR_RAY_RED, shift)
