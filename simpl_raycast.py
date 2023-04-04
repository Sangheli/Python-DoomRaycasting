import sys
import simple_raycast.render2D as render2D
from simple_raycast.variables import *
import simple_raycast.collision as _collision_

pygame.init()

def draw_3D_back():
    pygame.draw.rect(win, (100, 0, 0), (SHIFT_WIDTH, SCREEN_HEIGHT / 2, SCREEN_HEIGHT, SCREEN_HEIGHT))
    pygame.draw.rect(win, (200, 0, 0), (SHIFT_WIDTH, -SCREEN_HEIGHT / 2, SCREEN_HEIGHT, SCREEN_HEIGHT))

def draw_3D_wall_segment(ray, depth, start_angle):
    color = 50 / (1 + depth * depth * 0.0001)
    depth *= math.cos(player_angle - start_angle)
    wall_height = 21000 / (depth + 0.0001)
    if wall_height > SCREEN_HEIGHT: wall_height == SCREEN_HEIGHT

    pygame.draw.rect(win, (color, color, color), (
        SCREEN_HEIGHT + ray * SCALE, (SCREEN_HEIGHT / 2) - wall_height / 2, SCALE, wall_height))

def cast_rays():
    start_angle = player_angle - HALF_FOV

    for ray in range(CASTED_RAYS):
        for depth in range(MAX_DEPTH):
            target_x = player_x - math.sin(start_angle) * depth
            target_y = player_y + math.cos(start_angle) * depth
            col = int(target_x / TILE_SIZE)
            row = int(target_y / TILE_SIZE)
            index = row * MAP_SIZE + col

            if MAP[index] == wallID:
                render2D.draw_2D_rays(col, row, target_x, target_y,player_x,player_y)
                draw_3D_wall_segment(ray, depth, start_angle)
                break

        start_angle += STEP_ANGLE

def input_scan(player_angle,player_x,player_y,forward):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]: player_angle -= 0.1
    if keys[pygame.K_RIGHT]: player_angle += 0.1
    if keys[pygame.K_UP]:
        forward = True
        player_x += -math.sin(player_angle) * 5
        player_y += math.cos(player_angle) * 5
    if keys[pygame.K_DOWN]:
        forward = False
        player_x -= -math.sin(player_angle) * 5
        player_y -= math.cos(player_angle) * 5

    return player_angle,player_x,player_y,forward

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    player_x,player_y = _collision_.check_collision(player_x, player_y)
    render2D.draw_2D_map(player_x,player_y,player_angle)
    draw_3D_back()
    cast_rays()
    player_angle,player_x,player_y,forward = input_scan(player_angle,player_x,player_y,forward)
    clock.tick(60)
    fps = str(int(clock.get_fps()))
    font = pygame.font.SysFont('Monospace Regular', 30)
    textsurface = font.render(fps, False, (255, 255, 255))
    win.blit(textsurface, (0, 0))
    pygame.display.flip()
