import pygame
import simple_raycast.map as map
import simple_raycast.color as _color_
import simple_raycast.variables as _var_
import math

rect_back = (0,0,map.MAP_SIZE*_var_.TILE_SIZE_2D,map.MAP_SIZE*_var_.TILE_SIZE_2D)
back_surf = pygame.Surface(pygame.Rect(rect_back).size)

def prepare_surf():
    if not _var_.draw2D: return
    # back
    pygame.draw.rect(back_surf, _color_.black, (0, 0, _var_.SCREEN_HEIGHT, _var_.SCREEN_HEIGHT))

    # cells
    for row in range(map.MAP_SIZE):
        for col in range(map.MAP_SIZE):
            draw_2D_cell(back_surf, col, row)

def draw_2D_cell(surf, col, row):
    tile = (col,row)
    cur_color = _color_.cell1 if map.is_wall(tile) else _color_.cell2
    pygame.draw.rect(surf, cur_color,
                     (col * _var_.TILE_SIZE_2D, row * _var_.TILE_SIZE_2D, _var_.TILE_SIZE_2D - 2, _var_.TILE_SIZE_2D - 2))


def draw_2D_player_base_rays(surf,ox, oy, angle):
    pygame.draw.line(surf, _color_.green, (ox, oy),
                     (ox + math.cos(angle) * 50, oy + math.sin(angle) * 50), 3)
    pygame.draw.line(surf, _color_.green, (ox, oy), (
        ox + math.cos(angle - _var_.HALF_FOV) * 50,
        oy + math.sin(angle - _var_.HALF_FOV) * 50), 3)
    pygame.draw.line(surf, _color_.green, (ox, oy), (
        ox + math.cos(angle + _var_.HALF_FOV) * 50,
        oy + math.sin(angle + _var_.HALF_FOV) * 50), 3)


def draw_2D_map(player_x, player_y, player_angle):
    if not _var_.draw2D: return

    new_surf = pygame.Surface.copy(back_surf)

    # player dot
    pygame.draw.circle(new_surf, _color_.red, (int(player_x*_var_.TILE_MULT), int(player_y*_var_.TILE_MULT)), 8)
    draw_2D_player_base_rays(new_surf,int(player_x*_var_.TILE_MULT), int(player_y*_var_.TILE_MULT), player_angle)

    return new_surf

def draw_ray(new_surf,ox, oy, px, py):
    if not _var_.draw2D: return
    pygame.draw.line(new_surf, _color_.yellow,
                     (int(ox * _var_.TILE_MULT), int(oy * _var_.TILE_MULT)),
                     (int(px * _var_.TILE_MULT), int(py * _var_.TILE_MULT)))

def finish(new_surf):
    if not _var_.draw2D: return
    _var_.win.blit(new_surf, rect_back)