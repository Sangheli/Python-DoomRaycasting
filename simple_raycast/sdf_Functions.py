from math import sqrt
import numpy as np


def SignedDistance(a, b, r):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    distance = sqrt(dx**2 + dy**2)
    return distance - r


def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: return v
    return v / norm


def offScreen(current_vector, max_width, max_height):
    x = int(current_vector[0])
    y = int(current_vector[1])
    return x < 0 or x > max_width or y < 0 or y > max_height
