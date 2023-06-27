import pygame
from simple_raycast import map
from simple_raycast import color as _color_
from simple_raycast import variables as _var_
import math


def prepare_surf():
    if not _var_.draw2D: return

    rect_back = (0, 0, map.MAP_SIZE * _var_.TILE_SIZE_2D, map.MAP_SIZE * _var_.TILE_SIZE_2D)
    back_surf = pygame.Surface(pygame.Rect(rect_back).size)

    return back_surf


def draw_2D_player_base_rays(frame, ox, oy, angle):
    pygame.draw.line(frame, _color_.green, (ox, oy),
                     (ox + math.cos(angle) * 50, oy + math.sin(angle) * 50), 3)
    pygame.draw.line(frame, _color_.green, (ox, oy), (
        ox + math.cos(angle - _var_.HALF_FOV) * 50,
        oy + math.sin(angle - _var_.HALF_FOV) * 50), 3)
    pygame.draw.line(frame, _color_.green, (ox, oy), (
        ox + math.cos(angle + _var_.HALF_FOV) * 50,
        oy + math.sin(angle + _var_.HALF_FOV) * 50), 3)


def draw_2D_map(frame, surf2D, player_x, player_y, player_angle, objects):
    if not _var_.draw2D: return
    frame.blit(surf2D, (0, 0))
    # player dot
    pygame.draw.circle(frame, _color_.red, (int(player_x * _var_.TILE_MULT), int(player_y * _var_.TILE_MULT)), 8)
    draw_2D_player_base_rays(frame, int(player_x * _var_.TILE_MULT), int(player_y * _var_.TILE_MULT), player_angle)

    for obj in objects:
        if obj.position[0] < 0 or obj.position[1] < 0: continue
        pygame.draw.circle(frame, obj.color, (int(obj.position[0]), int(obj.position[1])), int(obj.radius))


def draw_ray(frame, ox, oy, depth, angle):
    if not _var_.draw2D: return

    px = ox + depth * math.cos(angle)
    py = oy + depth * math.sin(angle)

    pygame.draw.line(frame, _color_.yellow,
                     (int(ox * _var_.TILE_MULT), int(oy * _var_.TILE_MULT)),
                     (int(px * _var_.TILE_MULT), int(py * _var_.TILE_MULT)))
