import pygame as pg

_ = False
mini_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 2, 2, 2, 2, _, _, _, 3, 3, 3, _, _, 1],
    [1, _, _, _, _, _, 2, _, _, _, _, _, 3, _, _, 1],
    [1, _, _, _, _, 2, 2, _, _, _, _, _, 3, _, _, 1],
    [1, _, 4, 4, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, 4, _, 4, _, _, _, 5, 5, 5, 5, _, _, _, 1],
    [1, _, _, _, 4, _, _, _, 5, _, _, _, _, _, _, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]


class Map:
    def __init__(self, game):
        self.game = game
        self.mini_map = mini_map
        self.world_map = self.get_map()

    def get_map(self):
        world_map = {}

        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value:
                    world_map[(i, j)] = value

        return world_map

    def draw(self):
        [pg.draw.rect(self.game.screen, 'darkgray', (pos[0] * 100, pos[1] * 100, 100, 100), 2)
         for pos in self.world_map]
