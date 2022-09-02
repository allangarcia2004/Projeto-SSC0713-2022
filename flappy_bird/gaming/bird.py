from pygame.math import Vector2
from pygame.surface import Surface
import pygame

from .colors import Color


class Bird:
    GRAVITY = 2.25
    JUMP_SPEED = -20

    def __init__(self, screen: Surface, radius: float, initial_pos: tuple[int, int],
                 initial_vel: tuple[int, int] = (0, 0)):
        self.radius = radius
        self.screen = screen
        self.pos = Vector2(initial_pos)
        self.vel = Vector2(initial_vel)

    def update(self):
        self.vel.y += Bird.GRAVITY
        self.pos += self.vel

    def draw(self):
        pygame.draw.circle(self.screen, Color.YELLOW, self.pos, self.radius)

    def jump(self):
        self.vel.y = Bird.JUMP_SPEED
