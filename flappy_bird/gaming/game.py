import pygame
from pygame.event import Event
from pygame.math import Vector2

from .bird import Bird, BirdSharedData
from .colors import Color
from .world import WorldSharedData


class Game:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_size = Vector2(screen_width, screen_height)
        self.screen = pygame.display.set_mode(self.screen_size)

        self.closed = False
        self.clock = pygame.time.Clock()

        self.world_data = WorldSharedData(2.25, 1, self.screen_size, self.screen)

        self.bird_data = BirdSharedData(15.0, 21, 60, self.world_data)
        self.bird = Bird(self.bird_data)

    def on_event(self, event: Event):
        if event.type == pygame.QUIT:
            self.closed = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.bird.jump()

    def update(self):
        self.bird.verify_death(self.screen_size.y)
        self.bird.update()

    def draw(self):
        self.screen.fill(Color.BLACK)
        self.bird.draw()
        pygame.display.flip()

    def run(self):
        while not self.closed:
            self.clock.tick(30)
            for event in pygame.event.get():
                self.on_event(event)
            self.update()
            self.draw()
