import pygame
import sys
import simple_raycast.raycast as _raycast_
import simple_raycast.render2D as render2D
import simple_raycast.render3D as render3D
import simple_raycast.variables as _var_
import simple_raycast.collision as _collision_
import simple_raycast.input as _input_

pygame.init()
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    player_x, player_y, player_angle = _var_.player_x, _var_.player_y, _var_.player_angle
    forward = _var_.forward

    player_x, player_y = _collision_.check_collision(player_x, player_y, player_angle, forward)
    render2D.draw_2D_map(player_x, player_y, player_angle)
    render3D.draw_3D_back()
    _raycast_.cast_rays(player_x, player_y)

    _var_.player_angle, _var_.player_x, _var_.player_y, _var_.forward = _input_.input_scan(player_angle, player_x,
                                                                                           player_y, forward)

    clock.tick(60)
    fps = str(int(clock.get_fps()))
    font = pygame.font.SysFont('Monospace Regular', 30)
    textsurface = font.render(fps, False, (255, 255, 255))
    _var_.win.blit(textsurface, (0, 0))
    pygame.display.flip()
