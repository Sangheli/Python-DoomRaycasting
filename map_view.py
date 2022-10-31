import pygame as pg
from settings import *


class MapView:
    def __init__(self, game):
        self.game = game

    def draw(self):
        for pos in self.game.map.world_map:
            self.draw_cell(pos)

    def draw_cell(self, pos):
        pg.draw.rect(self.game.screen, COLOR_CELL, (pos[0] * CELL_SIZE, pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)