# https://pythonprogramming.altervista.org/raycasting-with-pygame/
# https://github.com/Josephbakulikira/2D-Raymarching-with-python-
import pygame
import sys
import sdf_raycast as _raycast_
from simple_raycast import render3D_solid_back
import sdf_render2D as render2D
import simple_raycast.variables as _var_
from simple_raycast import input as _input_
import numpy as np
from sdf_Boundary import Boundary
from random import randint

pygame.init()
clock = pygame.time.Clock()
DELTATIMEMS = 0
surf2D = render2D.prepare_surf()
main_frame = pygame.surfarray.make_surface(np.random.uniform(0, 1, _var_.rect_main_frame) * 255)

screen_offset = 50
object_count = 1
objects = []
objectsSq = []

for i in range(object_count):
    x = randint(screen_offset, _var_.SCREEN_WIDTH - screen_offset)
    y = randint(screen_offset, _var_.SCREEN_HEIGHT - screen_offset)

    obj = Boundary(
       x,
       y,
        60,
        False
    )
    objects.append(obj)

for i in range(object_count):
    obj = Boundary(
        x,
        y,
        50,
        True
    )
    objectsSq.append(obj)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    DELTATIME = DELTATIMEMS / 1000
    fixed_x, fixed_y = _var_.player_x, _var_.player_y

    # for obj in objects: obj.random_move(DELTATIME)

    render2D.draw_2D_map(main_frame, surf2D, fixed_x, fixed_y, _var_.player_angle,objects)
    render2D.draw_2D_map(main_frame, surf2D, fixed_x, fixed_y, _var_.player_angle,objectsSq)
    render3D_solid_back.draw_3D_back(main_frame)
    _raycast_.cast_rays(fixed_x, fixed_y, main_frame,objects,objectsSq)

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
