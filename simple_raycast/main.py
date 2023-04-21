# https://pythonprogramming.altervista.org/raycasting-with-pygame/
import pygame
import sys
import raycast as _raycast_
import render2D as render2D
import render3D as render3D
import variables as _var_
import collision as _collision_
import input as _input_
import numpy as np

pygame.init()
clock = pygame.time.Clock()
DELTATIMEMS = 0
surf2D = render2D.prepare_surf()
main_frame = pygame.surfarray.make_surface(np.random.uniform(0, 1, _var_.rect_main_frame) * 255)


def print_fps(frame):
    fps = 'numba: ' + str(int(clock.get_fps()))
    font = pygame.font.SysFont('Monospace Regular', 30)
    textsurface = font.render(fps, False, (255, 255, 255))
    frame.blit(textsurface, (0, 0))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    DELTATIME = DELTATIMEMS / 1000
    fixed_x, fixed_y = _collision_.check_collision(_var_.player_x, _var_.player_y, _var_.player_angle, _var_.forward,
                                                   DELTATIME)

    render3D.draw_3D_back(main_frame, _var_.player_angle, fixed_x, fixed_y)
    render2D.draw_2D_map(main_frame, surf2D, fixed_x, fixed_y, _var_.player_angle)
    raycount = _raycast_.cast_rays(fixed_x, fixed_y, main_frame)

    _var_.player_angle, _var_.player_x, _var_.player_y, _var_.forward = _input_.input_scan(_var_.player_angle, fixed_x,
                                                                                           fixed_y, _var_.forward,
                                                                                           DELTATIME)
    clock.tick(600)
    DELTATIMEMS = clock.get_time()

    screen_frame = pygame.transform.scale(main_frame,
                                          (_var_.rect_main_frame_scaled[0], _var_.rect_main_frame_scaled[1]))
    _var_.win.blit(screen_frame, (0, 0))
    pygame.display.flip()
    pygame.display.set_caption(f'{clock.get_fps():.2f} | rays: {raycount}')
