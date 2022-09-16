import pygame
from pygame.event import Event
from pygame import Vector2

from .bird import Bird, BirdSharedData
from .colors import Color
from .pipe import PipeSharedData, Pipe
from .world import WorldSharedData


class Game:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_size = Vector2(screen_width, screen_height)
        self.screen = pygame.display.set_mode(self.screen_size)

        self.closed = False
        self.clock = pygame.time.Clock()

        self.world_data = WorldSharedData(2.25, 5, self.screen_size, self.screen)

        self.bird_data = BirdSharedData(15.0, 21, 100, self.world_data)
        self.bird = Bird(self.bird_data)

        self.pipe_data = PipeSharedData(40, 140, self.world_data)
        self.pipe = Pipe(self.pipe_data)

    def handle_event(self, event: Event):
        if event.type == pygame.QUIT:
            self.closed = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.bird.jump()

    def update(self):
        if self.pipe.collided_with_bird(self.bird):
            self.bird.dead = True
            self.closed = True
        self.bird.verify_death(self.screen_size.y)
        self.bird.update()
        self.pipe.update()

    def draw(self):
        self.screen.fill(Color.BLACK)
        self.bird.draw()
        self.pipe.draw()
        pygame.display.flip()

    def run(self):
        while not self.closed:
            self.clock.tick(30)
            for event in pygame.event.get():
                self.handle_event(event)
            self.update()
            self.draw()
