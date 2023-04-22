# https://pythonprogramming.altervista.org/raycasting-with-pygame/
# https://github.com/Josephbakulikira/2D-Raymarching-with-python-
import pygame
import sys
import sdf_raycast as _raycast_
import render3D_solid_back
import variables as _var_
import input as _input_
import numpy as np
from sdf_Boundary import Boundary
from random import randint

pygame.init()
clock = pygame.time.Clock()
DELTATIMEMS = 0
main_frame = pygame.surfarray.make_surface(np.random.uniform(0, 1, _var_.rect_main_frame) * 255)

screen_offset = 50
object_count = 10
objects = []

for i in range(object_count):
    obj = Boundary(randint(screen_offset, _var_.SCREEN_WIDTH - screen_offset), randint(screen_offset, _var_.SCREEN_HEIGHT - screen_offset), randint(5, 70))
    objects.append(obj)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    DELTATIME = DELTATIMEMS / 1000
    fixed_x, fixed_y = _var_.player_x, _var_.player_y

    render3D_solid_back.draw_3D_back(main_frame)

    for obj in objects:
        obj.random_move(DELTATIME)

    _raycast_.cast_rays(fixed_x, fixed_y, main_frame,objects)

    _var_.player_angle, _var_.player_x, _var_.player_y, _var_.forward = _input_.input_scan(_var_.player_angle, fixed_x,
                                                                                           fixed_y, _var_.forward,
                                                                                           DELTATIME)
    clock.tick(600)
    DELTATIMEMS = clock.get_time()

    screen_frame = pygame.transform.scale(main_frame,
                                          (_var_.rect_main_frame_scaled[0], _var_.rect_main_frame_scaled[1]))
    _var_.win.blit(screen_frame, (0, 0))
    pygame.display.flip()
    pygame.display.set_caption(f'{clock.get_fps():.2f}')
