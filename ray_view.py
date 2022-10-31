import pygame as pg

class RayView:
    def __init__(self, game):
        self.game = game

    def draw(self, x, y, width, sin_a, cos_a, COLOR):
        start = (x, y)
        shift_x, shift_y = width * cos_a, width * sin_a
        end = (x + shift_x, y + shift_y)
        pg.draw.line(self.game.screen, COLOR, start, end, 2)