import pygame as pg
import math
from settings import *


def get_projection_height(depth):
    return SCREEN_DIST / (depth + 0.0001)


class RayCasting:
    def __init__(self, game):
        self.game = game
        self.ray_casting_result = []
        self.objects_to_render = []
        self.textures = self.game.object_renderer.wall_textures

    def get_objects_to_render(self):
        self.objects_to_render = []
        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset = values

            if proj_height < HEIGHT:
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                )

                wall_column = pg.transform.scale(wall_column, (SCALE, proj_height))
                wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)
            else:
                texture_height = TEXTURE_SIZE * HEIGHT / proj_height
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), HALF_TEXTURE_SIZE - texture_height // 2,
                    SCALE, texture_height
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, HEIGHT))
                wall_pos = (ray * SCALE, 0)

            self.objects_to_render.append((depth, wall_column, wall_pos))

    def ray_cast(self):
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos
        ray_angle = self.get_angle()
        self.ray_casting_result = self.iterate_rays(ray_angle, ox, oy, x_map, y_map)

    def iterate_rays(self, angle, ox, oy, x_map, y_map):
        ray_casting_result = []

        for ray in range(NUM_RAYS):
            ray_angle = angle + ray * DELTA_ANGLE
            sin_a, cos_a = math.sin(ray_angle), math.cos(ray_angle)

            depth, texture, offset = self.process_ray(ox, oy, x_map, y_map, sin_a, cos_a)
            depth = self.fix_fisheye(depth, ray_angle)

            proj_height = get_projection_height(depth)

            self.game.render.render_raycast(ox, oy, depth, sin_a, cos_a, ray, proj_height)
            ray_casting_result.append((depth, proj_height, texture, offset))

        return ray_casting_result

    def process_ray(self, ox, oy, x_map, y_map, sin_a, cos_a):
        x_hor, y_hor, dx, dy, depth_hor, delta_depth = self.process_depth(y_map, sin_a, cos_a, ox, oy)
        x_hor, _, depth_hor, texture_hor = self.process_depth_texture(x_hor, y_hor, dx, dy, depth_hor, delta_depth)

        y_vert, x_vert, dy, dx, depth_vert, delta_depth = self.process_depth(x_map, cos_a, sin_a, oy, ox)
        _, y_vert, depth_vert, texture_vert = self.process_depth_texture(x_vert, y_vert, dx, dy, depth_vert, delta_depth)

        if depth_vert < depth_hor:
            depth, texture = depth_vert, texture_vert
            y_vert %= 1
            offset = y_vert if cos_a > 0 else (1 - y_vert)
        else:
            depth, texture = depth_hor, texture_hor
            x_hor %= 1
            offset = (1 - x_hor) if sin_a > 0 else x_hor

        return depth, texture, offset

    def process_depth_texture(self, x, y, dx, dy, depth, delta_depth):
        texture_shift = 1
        max_i = 0

        for i in range(MAX_DEPTH):
            tile_hor = int(x + i * dx), int(y + i * dy)
            if tile_hor in self.game.map.world_map:
                texture_shift = self.game.map.world_map[tile_hor]
                break
            max_i = i + 1

        x += dx * max_i
        y += dy * max_i
        depth += delta_depth * max_i
        return x, y, depth, texture_shift

    def process_depth(self, map_item, sin_a, cos_a, ox, oy):
        y_hor, dy = (map_item + 1, 1) if sin_a > 0 else (map_item - 1e-6, -1)
        depth_hor = (y_hor - oy) / sin_a
        x_hor = ox + depth_hor * cos_a
        delta_depth = dy / sin_a
        dx = delta_depth * cos_a
        return x_hor, y_hor, dx, dy, depth_hor, delta_depth

    def get_angle(self):
        return self.game.player.angle - HALF_FOV + 0.0001

    def fix_fisheye(self, depth, ray_angle):
        if self.game.render_type is not RenderType.TwoD:
            depth *= math.cos(self.game.player.angle - ray_angle)

        return depth

    def update(self):
        self.ray_cast()
        if self.game.render_type == RenderType.WallsTextures:
            self.get_objects_to_render()
