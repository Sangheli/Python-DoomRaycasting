import pygame
import numpy as np
import color as _color_


def draw_reflection(frame, rect, shading, obj):
    color = _color_.color_reflection if obj is None else get_obj_color(obj)
    rect_reflected = np.array(rect)
    rect_reflected[1] = rect_reflected[1] + rect_reflected[3]
    shape_surf = pygame.Surface(pygame.Rect(rect_reflected).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, _color_.get_color_with_shading(color, shading),
                     shape_surf.get_rect())
    frame.blit(shape_surf, rect_reflected)


def get_obj_color(obj):
    return obj.color[0] * 0.4, obj.color[1] * 0.4, obj.color[2] * 0.4, 122
