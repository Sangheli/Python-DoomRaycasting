import pygame as pg
import numpy as np
import math

# settings
res = width, height = 160, 100
offset = np.array([1.3 * width, height]) // 2
max_iter = 30
zoom = 2.2 / height


class Fractal:
    def __init__(self, app):
        self.app = app
        self.screen_array = np.full((width, height, 3), [0, 0, 0], dtype=np.uint8)

    def render(self):
        for x in range(width):
            for y in range(height):
                c = (x - offset[0]) * zoom + 1j * (y - offset[1]) * zoom
                z = 0
                num_iter = 0
                for i in range(max_iter):
                    z = z ** 2 + c
                    if abs(z) > 2:
                        break
                    num_iter += 1
                col = int(255 * num_iter / max_iter)
                self.screen_array[x, y] = (col, col, col)

    def update(self):
        self.render()

    def draw(self):
        pg.surfarray.blit_array(self.app.screen, self.screen_array)

    def run(self):
        self.update()
        self.draw()


class App:
    def __init__(self):
        self.screen = pg.display.set_mode(res, pg.SCALED)
        self.clock = pg.time.Clock()
        self.fractal = Fractal(self)

    def run(self):
        while True:
            self.screen.fill('black')
            self.fractal.run()
            pg.display.flip()

            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            self.clock.tick()
            pg.display.set_caption(f'FPS: {self.clock.get_fps()}')


if __name__ == '__main__':
    app = App()
    app.run()
