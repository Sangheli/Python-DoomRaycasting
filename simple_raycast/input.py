import pygame
import math
import variables as _var_


def input_scan(player_angle, player_x, player_y, forward,DELTATIME):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]: player_angle -= _var_.PLAYER_ROT_SPEED * DELTATIME
    if keys[pygame.K_RIGHT]: player_angle += _var_.PLAYER_ROT_SPEED * DELTATIME
    if keys[pygame.K_UP]:
        forward = True
        player_x += math.cos(player_angle) * _var_.PLAYER_SPEED * DELTATIME
        player_y += math.sin(player_angle) * _var_.PLAYER_SPEED * DELTATIME
    if keys[pygame.K_DOWN]:
        forward = False
        player_x -= math.cos(player_angle) * _var_.PLAYER_SPEED * DELTATIME
        player_y -= math.sin(player_angle) * _var_.PLAYER_SPEED * DELTATIME

    return player_angle, player_x, player_y, forward
