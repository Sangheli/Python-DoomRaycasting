import pygame
import simple_raycast.map as map
import simple_raycast.color as _color_
import simple_raycast.variables as _var_
import math


def draw_2D_cell(col, row):
    cur_color = _color_.cell1 if map.is_wall(col,row) else _color_.cell2
    pygame.draw.rect(_var_.win, cur_color,
                     (col * _var_.TILE_SIZE, row * _var_.TILE_SIZE, _var_.TILE_SIZE - 2, _var_.TILE_SIZE - 2))


def draw_2D_player_base_rays(player_x, player_y, player_angle):
    pygame.draw.line(_var_.win, _color_.green, (player_x, player_y),
                     (player_x - math.sin(player_angle) * 50, player_y + math.cos(player_angle) * 50), 3)
    pygame.draw.line(_var_.win, _color_.green, (player_x, player_y), (
        player_x - math.sin(player_angle - _var_.HALF_FOV) * 50,
        player_y + math.cos(player_angle - _var_.HALF_FOV) * 50), 3)
    pygame.draw.line(_var_.win, _color_.green, (player_x, player_y), (
        player_x - math.sin(player_angle + _var_.HALF_FOV) * 50,
        player_y + math.cos(player_angle + _var_.HALF_FOV) * 50), 3)


def draw_2D_map(player_x, player_y, player_angle):
    if not _var_.draw2D: return

    # back
    pygame.draw.rect(_var_.win, _color_.black, (0, 0, _var_.SCREEN_HEIGHT, _var_.SCREEN_HEIGHT))

    # cells
    for row in range(map.MAP_SIZE):
        for col in range(map.MAP_SIZE):
            draw_2D_cell(col, row)

    # player dot
    pygame.draw.circle(_var_.win, _color_.red, (int(player_x), int(player_y)), 8)
    draw_2D_player_base_rays(player_x, player_y, player_angle)


def draw_2D_rays(col, row, target_x, target_y, player_x, player_y):
    if not _var_.draw2D: return
    pygame.draw.rect(_var_.win, _color_.green,
                     (col * _var_.TILE_SIZE, row * _var_.TILE_SIZE, _var_.TILE_SIZE - 2, _var_.TILE_SIZE - 2))
    pygame.draw.line(_var_.win, _color_.yellow, (player_x, player_y), (target_x, target_y))
