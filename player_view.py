import pygame as pg
from settings import *


class PlayerView:
    def __init__(self, game):
        self.game = game

    def render(self):
        self.draw_player(self.game.player.x, self.game.player.y)
        self.draw_player_ray(self.game.player.x, self.game.player.y, self.game.player.angle)

    def draw_player(self, x, y):
        pg.draw.circle(self.game.screen, COLOR_PLAYER, (x * CELL_SIZE, y * CELL_SIZE), 15)

    def draw_player_ray(self, x, y, angle):
        start_x, start_y = CELL_SIZE * x, CELL_SIZE * y
        sin_a = math.sin(angle)
        cos_a = math.cos(angle)
        self.game.ray_view.draw(start_x, start_y, WIDTH, sin_a, cos_a, COLOR_RAY_RED)
