import pygame
import simple_raycast.map as map
import simple_raycast.color as _color_
import simple_raycast.variables as _var_
import math


def prepare_surf():
    if not _var_.draw2D: return

    rect_back = (0, 0, map.MAP_SIZE * _var_.TILE_SIZE_2D, map.MAP_SIZE * _var_.TILE_SIZE_2D)
    back_surf = pygame.Surface(pygame.Rect(rect_back).size)

    # back
    pygame.draw.rect(back_surf, _color_.black, (0, 0, _var_.SCREEN_HEIGHT, _var_.SCREEN_HEIGHT))

    # cells
    for row in range(map.MAP_SIZE):
        for col in range(map.MAP_SIZE):
            draw_2D_cell(back_surf, col, row)

    return back_surf


def draw_2D_cell(surf, col, row):
    tile = (col, row)
    cur_color = _color_.cell1 if map.is_wall(tile) else _color_.cell2
    pygame.draw.rect(surf, cur_color,
                     (col * _var_.TILE_SIZE_2D, row * _var_.TILE_SIZE_2D, _var_.TILE_SIZE_2D - 2,
                      _var_.TILE_SIZE_2D - 2))


def draw_2D_player_base_rays(frame, ox, oy, angle):
    pygame.draw.line(frame, _color_.green, (ox, oy),
                     (ox + math.cos(angle) * 50, oy + math.sin(angle) * 50), 3)
    pygame.draw.line(frame, _color_.green, (ox, oy), (
        ox + math.cos(angle - _var_.HALF_FOV) * 50,
        oy + math.sin(angle - _var_.HALF_FOV) * 50), 3)
    pygame.draw.line(frame, _color_.green, (ox, oy), (
        ox + math.cos(angle + _var_.HALF_FOV) * 50,
        oy + math.sin(angle + _var_.HALF_FOV) * 50), 3)


def draw_2D_map(frame, surf2D, player_x, player_y, player_angle):
    if not _var_.draw2D: return
    frame.blit(surf2D, (0, 0))
    # player dot
    pygame.draw.circle(frame, _color_.red, (int(player_x * _var_.TILE_MULT), int(player_y * _var_.TILE_MULT)), 8)
    draw_2D_player_base_rays(frame, int(player_x * _var_.TILE_MULT), int(player_y * _var_.TILE_MULT), player_angle)


def draw_ray(frame, ox, oy, px, py):
    if not _var_.draw2D: return
    pygame.draw.line(frame, _color_.yellow,
                     (int(ox * _var_.TILE_MULT), int(oy * _var_.TILE_MULT)),
                     (int(px * _var_.TILE_MULT), int(py * _var_.TILE_MULT)))
