from map import *
from map_view import *
from player import *
from player_view import *
from raycasting import *
from object_renderer import *
from render import *
from input import *
from textureloader import *
from ray_view import *


class Game:
    def __init__(self):
        pg.init()
        self.render_type = RENDER_TYPE
        pg.mouse.set_visible(self.render_type is RenderType.TwoD)
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.new_game()

    def new_game(self):
        self.ray_view = RayView(self)
        self.map = Map(self)
        self.map_view = MapView(self)
        self.player = Player(self)
        self.player_view = PlayerView(self)
        self.textureloader = TextureLoader(self)
        self.object_renderer = ObjectRenderer(self)
        self.render = Render(self)
        self.raycasting = RayCasting(self)
        self.input = Input(self)

    def update(self):
        self.player.update()
        self.raycasting.update()
        pg.display.flip()
        self.print_window_header()

    def print_window_header(self):
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def run(self):
        while True:
            self.input.check_events()
            self.update()
            self.render.draw()


if __name__ == '__main__':
    game = Game()
    game.run()
