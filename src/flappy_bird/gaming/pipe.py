from random import randint

import pygame
from pygame import Rect

from flappy_bird.gaming.colors import Color
from flappy_bird.gaming.world import WorldSharedData


class PipeSharedData:
    def __init__(self, width: int, gap_size: int, world_data: WorldSharedData):
        self.width = width
        self.gap_size = gap_size
        self.world_data = world_data


class Pipe:
    MIN_LENGTH = 50

    def __init__(self, shared_data: PipeSharedData):
        self.shared_data = shared_data
        self.x_pos = 0
        self.gap_y_pos = 0

        self.top_rect = self.get_top_rect()
        self.bottom_rect = self.get_bottom_rect()

        self.reset_positions()

    def reset_positions(self):
        self.x_pos = self.shared_data.world_data.screen_size.x
        self.gap_y_pos = randint(
            self.MIN_LENGTH,
            int(self.shared_data.world_data.screen_size.y - self.shared_data.gap_size - self.MIN_LENGTH))

    def get_top_rect(self):
        return Rect(self.x_pos, 0, self.shared_data.width, self.gap_y_pos)

    def get_bottom_rect(self):
        top = self.gap_y_pos + self.shared_data.gap_size
        height = self.shared_data.world_data.screen_size.y - top
        return Rect(self.x_pos, top, self.shared_data.width, height)

    def update(self):
        self.x_pos -= self.shared_data.world_data.horizontal_velocity
        if self.x_pos + self.shared_data.width < 0:
            self.reset_positions()
        self.top_rect = self.get_top_rect()
        self.bottom_rect = self.get_bottom_rect()

    def draw(self):
        pygame.draw.rect(self.shared_data.world_data.screen, Color.WHITE, self.top_rect)
        pygame.draw.rect(self.shared_data.world_data.screen, Color.WHITE, self.bottom_rect)
