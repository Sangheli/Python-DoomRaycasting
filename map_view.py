import pygame as pg
from settings import *


class MapView:
    def __init__(self, game):
        self.game = game

    def draw(self):
        for pos in self.game.map.world_map:
            self.draw_cell(pos,MAP_SHIFT_X,MAP_SHIFT_Y)

    def draw_cell(self, pos,shiftx,shifty):
        pg.draw.rect(self.game.screen, COLOR_CELL, (shiftx + pos[0] * CELL_SIZE, shifty + pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)