import math
import random

speed = 50


class Boundary:
    def __init__(self, x, y, radius):
        self.position = [x, y]
        self.radius = radius
        self.step_count = 0
        self.delta = [0, 0]
        self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))

    def random_move(self, DELTATIME):
        if self.step_count == 0: self.delta = [random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)]
        self.position[0] += self.delta[0] * speed * DELTATIME
        self.position[1] += self.delta[1] * speed * DELTATIME
        self.step_count += 1
        if self.step_count > 20: self.step_count = 0

    def SignedDistance(self, target_pos):
        dx = target_pos[0] - self.position[0]
        dy = target_pos[1] - self.position[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)
        return distance - self.radius
