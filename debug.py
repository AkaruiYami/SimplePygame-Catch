import pygame

from settings import *


def draw_lane_line(window, color=(255, 255, 255)):
    for line in LANES[1:]:
        pygame.draw.line(window, color, (line, 0), (line, HEIGHT))


def draw_fall_line(window, color=(0, 150, 0)):
    _center_x = [line + LANE_SIZE // 2 for line in LANES]
    for x in _center_x:
        pygame.draw.line(window, color, (x, 0), (x, HEIGHT - 55))


def draw_door_collision(window, color=(150, 0, 0)):
    _center_x = [line + LANE_SIZE // 2 - 32 for line in LANES]
    _actual_position = [(_x, HEIGHT - 64) for _x in _center_x]
    for position in _actual_position:
        _rect = pygame.Rect(position[0], position[1], 64, 32)
        pygame.draw.rect(window, color, _rect, 1)
