from pygame.math import Vector2
import pygame

from .colors import Color
from .world import WorldSharedData


class BirdSharedData:
    def __init__(self, radius: float, bump_speed: float, horizontal_position: int, world_data: WorldSharedData):
        self.radius = radius
        self.bump_speed = bump_speed
        self.horizontal_position = horizontal_position
        self.world_data = world_data


class Bird:
    def __init__(self, shared_data: BirdSharedData):
        self.shared_data = shared_data
        self.pos = Vector2(self.shared_data.horizontal_position, self.shared_data.world_data.screen_size.y // 2)
        self.vel = Vector2(0, 0)
        self.dead = False

    def update(self):
        if not self.dead:
            self.vel.y += self.shared_data.world_data.gravity
        self.pos += self.vel

    def draw(self):
        pygame.draw.circle(self.shared_data.world_data.screen, Color.YELLOW, self.pos, self.shared_data.radius)

    def jump(self):
        self.vel.y = -self.shared_data.bump_speed

    def verify_death(self, screen_height: float):
        if self.pos.y - self.shared_data.radius <= 0 or self.pos.y + self.shared_data.radius >= screen_height:
            self.dead = True
            self.vel = Vector2(-self.shared_data.world_data.horizontal_speed, 0)
