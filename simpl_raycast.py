# https://pythonprogramming.altervista.org/raycasting-with-pygame/
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
DELTATIMEMS = 0

def print_fps():
    fps = 'numba: ' +str(int(clock.get_fps()))
    font = pygame.font.SysFont('Monospace Regular', 30)
    textsurface = font.render(fps, False, (255, 255, 255))
    _var_.win.blit(textsurface, (0, 0))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    DELTATIME = DELTATIMEMS/1000
    fixed_x, fixed_y = _collision_.check_collision(_var_.player_x, _var_.player_y, _var_.player_angle, _var_.forward,DELTATIME)

    render3D.draw_3D_back(_var_.player_angle)
    render2D.draw_2D_map(fixed_x, fixed_y, _var_.player_angle)
    
    _raycast_.cast_rays(fixed_x, fixed_y)

    _var_.player_angle, _var_.player_x, _var_.player_y, _var_.forward = _input_.input_scan(_var_.player_angle, fixed_x,
                                                                                           fixed_y, _var_.forward,
                                                                                           DELTATIME)
    clock.tick(600)
    DELTATIMEMS = clock.get_time()
    print_fps()
    pygame.display.flip()
