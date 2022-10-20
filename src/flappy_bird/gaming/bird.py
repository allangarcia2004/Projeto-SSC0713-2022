import pygame
from pygame import Vector2

from flappy_bird.gaming.collision import collided_circle_rect
from flappy_bird.gaming.colors import Color
from flappy_bird.gaming.pipe import Pipe
from flappy_bird.gaming.world import WorldSharedData


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
        self.alive = True

    def update(self):
        if self.alive:
            self.vel.y += self.shared_data.world_data.gravity
        self.pos += self.vel

    def draw(self):
        pygame.draw.circle(
            self.shared_data.world_data.screen,
            Color.YELLOW,
            self.pos,
            self.shared_data.radius,
        )

    def jump(self):
        self.vel.y = -self.shared_data.bump_speed

    def collided_with_pipe(self, pipe: Pipe):
        collided_top_rect = collided_circle_rect(self.pos, self.shared_data.radius, pipe.top_rect)
        collided_bottom_rect = collided_circle_rect(self.pos, self.shared_data.radius, pipe.bottom_rect)
        return collided_top_rect or collided_bottom_rect

    def crossed_screen_bounds(self):
        screen_height = self.shared_data.world_data.screen_size.y

        crossed_upper_bound = self.pos.y - self.shared_data.radius <= 0
        crossed_lower_bound = self.pos.y + self.shared_data.radius >= screen_height

        return crossed_lower_bound or crossed_upper_bound

    def died_now(self, pipe: Pipe):
        if not self.alive:
            return False

        if self.crossed_screen_bounds() or self.collided_with_pipe(pipe):
            self.alive = False
            self.vel = Vector2(-self.shared_data.world_data.horizontal_velocity, 0)
            return True

        return False
