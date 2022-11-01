import pygame as pg
import math
from settings import *


def get_projection_height(depth):
    return SCREEN_DIST / (depth + 0.0001)


def process_depth(map_item, func_a_1, func_a_2, x, y):
    line_2, delta2 = (map_item + 1, 1) if func_a_1 > 0 else (map_item - 1e-6, -1)
    depth = (line_2 - y) / func_a_1
    line_1 = x + depth * func_a_2

    delta_depth = delta2 / func_a_1
    delta1 = delta_depth * func_a_2

    return line_1, line_2, delta1, delta2, depth, delta_depth


class RayCasting:
    def __init__(self, game):
        self.game = game
        self.ray_casting_result = []
        self.objects_to_render = []
        self.textures = self.game.object_renderer.wall_textures

    def get_objects_to_render(self):
        self.objects_to_render = []
        for i, values in enumerate(self.ray_casting_result):
            depth, projection_height, wall_id, texture_offset = values
            final_height = projection_height if projection_height < HEIGHT else HEIGHT

            if projection_height < HEIGHT:
                wall_column_texture = self.extract_texture_part(wall_id, texture_offset, 0, TEXTURE_SIZE)
                screen_wall_pos = (i * COLUMN_SIZE_X, HALF_HEIGHT - projection_height // 2)
            else:
                texture_height = TEXTURE_SIZE * HEIGHT / projection_height
                startY = HALF_TEXTURE_SIZE - texture_height // 2
                wall_column_texture = self.extract_texture_part(wall_id, texture_offset, startY, texture_height)
                screen_wall_pos = (i * COLUMN_SIZE_X, 0)

            wall_column_texture = pg.transform.scale(wall_column_texture, (COLUMN_SIZE_X, final_height))
            self.objects_to_render.append((depth, wall_column_texture, screen_wall_pos))

    def extract_texture_part(self, wall_id, texture_offset, startY, height):
        return self.textures[wall_id].subsurface(
            texture_offset * (TEXTURE_SIZE - COLUMN_SIZE_X),
            startY,
            COLUMN_SIZE_X,
            height
        )

    def ray_cast(self):
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos
        ray_angle = self.get_angle()
        self.ray_casting_result = self.iterate_rays(ray_angle, ox, oy, x_map, y_map)

    def iterate_rays(self, angle, x, y, x_map, y_map):
        ray_casting_result = []

        for i in range(NUM_RAYS):
            ray_angle = angle + i * DELTA_ANGLE
            sin_a, cos_a = math.sin(ray_angle), math.cos(ray_angle)

            depth, wall_id, texture_offset = self.process_ray(x, y, x_map, y_map, sin_a, cos_a)

            depth = self.fix_fisheye(depth, ray_angle)
            projection_height = get_projection_height(depth)

            self.game.render.render_raycast(x, y, depth, sin_a, cos_a, i, projection_height)
            ray_casting_result.append((depth, projection_height, wall_id, texture_offset))

        return ray_casting_result

    def process_ray(self, ox, oy, x_map, y_map, sin_a, cos_a):
        x_hor, y_hor, dx, dy, depth_x, delta_depth = process_depth(y_map, sin_a, cos_a, ox, oy)
        x_hor, _, depth_x, wall_id_x = self.process_depth_texture(x_hor, y_hor, dx, dy, depth_x, delta_depth)

        y_vert, x_vert, dy, dx, depth_y, delta_depth = process_depth(x_map, cos_a, sin_a, oy, ox)
        _, y_vert, depth_y, wall_id_y = self.process_depth_texture(x_vert, y_vert, dx, dy, depth_y, delta_depth)

        if depth_y < depth_x:
            return depth_y, wall_id_y, y_vert % 1
        else:
            return depth_x, wall_id_x, x_hor % 1

    def process_depth_texture(self, x, y, dx, dy, depth, delta_depth):
        texture_id = 1
        max_i = 0

        for i in range(MAX_DEPTH):
            tile_hor = int(x + i * dx), int(y + i * dy)
            if tile_hor in self.game.map.world_map:
                texture_id = self.game.map.world_map[tile_hor]
                break
            max_i = i + 1

        x += dx * max_i
        y += dy * max_i
        depth += delta_depth * max_i
        return x, y, depth, texture_id

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
