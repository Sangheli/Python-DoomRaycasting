import pygame
import numpy as np
import color as _color_


def draw_reflection(frame, rect, shading):
    rect_reflected = np.array(rect)
    rect_reflected[1] = rect_reflected[1] + rect_reflected[3]
    shape_surf = pygame.Surface(pygame.Rect(rect_reflected).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, _color_.get_color_with_shading(_color_.color_reflection, shading),
                     shape_surf.get_rect())
    frame.blit(shape_surf, rect_reflected)
