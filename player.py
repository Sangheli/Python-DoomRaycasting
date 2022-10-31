from settings import *
import pygame as pg
import math


class Player:
    def __init__(self, game):
        self.rel = None
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE

    def movement(self):
        dx, dy = 0, 0
        sin_a, cos_a = math.sin(self.angle), math.cos(self.angle)
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin, speed_cos = speed * sin_a, speed * cos_a

        keys = pg.key.get_pressed()

        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin

        if keys[pg.K_s]:
            dx += -speed_cos
            dy += -speed_sin

        if keys[pg.K_a]:
            dx += speed_sin
            dy += -speed_cos

        if keys[pg.K_d]:
            dx += -speed_sin
            dy += speed_cos

        return dx, dy

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_colission(self, dx, dy):
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    def mouse_rotate(self):
        mx, my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WITH, HALF_HEIGHT])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time

    def keyboard_rotate(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
        if keys[pg.K_RIGHT]:
            self.angle += PLAYER_ROT_SPEED * self.game.delta_time

        self.angle %= math.tau

    def update(self):
        dx, dy = self.movement()

        if self.game.render_type is RenderType.TwoD:
            self.keyboard_rotate()
        else:
            self.mouse_rotate()

        self.check_wall_colission(dx, dy)

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)
