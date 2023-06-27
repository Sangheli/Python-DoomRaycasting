import numpy as np
import pygame as pg


class RayView:
    def __init__(self, game):
        self.game = game

    def draw(self, pos, depth, sin_a, cos_a, COLOR,shift):
        np_shift = np.array(shift)
        np_start = np.array(pos)
        np_len = np.array(depth)*np.array([cos_a,sin_a])
        np_end = np_start+np_shift+np_len
        pg.draw.line(self.game.screen, COLOR, np_start, np_end, 2)