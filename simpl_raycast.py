import pygame
import math
import sys
import simple_raycast.render2D as render2D
import simple_raycast.variables as _var_
import simple_raycast.collision as _collision_
import simple_raycast.input as _input_

pygame.init()
clock = pygame.time.Clock()

def draw_3D_back():
    pygame.draw.rect(_var_.win, (100, 0, 0),
                     (_var_.SHIFT_WIDTH, _var_.SCREEN_HEIGHT / 2, _var_.SCREEN_HEIGHT, _var_.SCREEN_HEIGHT))
    pygame.draw.rect(_var_.win, (200, 0, 0),
                     (_var_.SHIFT_WIDTH, -_var_.SCREEN_HEIGHT / 2, _var_.SCREEN_HEIGHT, _var_.SCREEN_HEIGHT))


def draw_3D_wall_segment(ray, depth, start_angle):
    color = 50 / (1 + depth * depth * 0.0001)
    depth *= math.cos(_var_.player_angle - start_angle)
    wall_height = 21000 / (depth + 0.0001)
    if wall_height > _var_.SCREEN_HEIGHT: wall_height == _var_.SCREEN_HEIGHT

    pygame.draw.rect(_var_.win, (color, color, color), (
        _var_.SCREEN_HEIGHT + ray * _var_.SCALE, (_var_.SCREEN_HEIGHT / 2) - wall_height / 2, _var_.SCALE, wall_height))


def cast_rays(player_x, player_y):
    start_angle = _var_.player_angle - _var_.HALF_FOV

    for ray in range(_var_.CASTED_RAYS):
        for depth in range(_var_.MAX_DEPTH):
            target_x = player_x - math.sin(start_angle) * depth
            target_y = player_y + math.cos(start_angle) * depth
            col = int(target_x / _var_.TILE_SIZE)
            row = int(target_y / _var_.TILE_SIZE)
            index = row * _var_.MAP_SIZE + col

            if _var_.MAP[index] == _var_.wallID:
                render2D.draw_2D_rays(col, row, target_x, target_y, player_x, player_y)
                draw_3D_wall_segment(ray, depth, start_angle)
                break

        start_angle += _var_.STEP_ANGLE


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    player_x,player_y,player_angle = _var_.player_x,_var_.player_y,_var_.player_angle

    forward = _var_.forward
    player_x, player_y = _collision_.check_collision(player_x, player_y, player_angle,forward)
    render2D.draw_2D_map(player_x, player_y, player_angle)
    draw_3D_back()
    cast_rays(player_x, player_y)

    _var_.player_angle, _var_.player_x, _var_.player_y, _var_.forward = _input_.input_scan(player_angle, player_x, player_y,forward)

    clock.tick(60)
    fps = str(int(clock.get_fps()))
    font = pygame.font.SysFont('Monospace Regular', 30)
    textsurface = font.render(fps, False, (255, 255, 255))
    _var_.win.blit(textsurface, (0, 0))
    pygame.display.flip()
