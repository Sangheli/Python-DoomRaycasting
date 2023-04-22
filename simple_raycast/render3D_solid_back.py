import pygame
import color as _color_
import variables as _var_


def draw_solid_sky(frame):
    pygame.draw.rect(frame, _color_.backSky,
                     (_var_.SCREEN_START[0], -_var_.SCREEN_START[1], _var_.SCREEN_WIDTH, _var_.SCREEN_HEIGHT))


def draw_solid_floor(frame):
    pygame.draw.rect(frame, _color_.backGround,
                     (_var_.SCREEN_START[0], _var_.SCREEN_START[1], _var_.SCREEN_WIDTH, _var_.SCREEN_HEIGHT))


def draw_3D_back(frame):
    draw_solid_floor(frame)
    draw_solid_sky(frame)
