import pygame
from pygame.math import Vector2

from .bird import Bird
from .colors import Color


class Game:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_size = Vector2(screen_width, screen_height)
        self.screen = pygame.display.set_mode(self.screen_size)

        self.closed = False
        self.clock = pygame.time.Clock()

        self.bird = Bird(self.screen, 15, (60, screen_height // 2))

    def run(self):
        while not self.closed and not self.bird.died:
            self.clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.closed = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.bird.jump()

            self.screen.fill(Color.BLACK)

            self.bird.verify_death(self.screen_size.y)
            self.bird.update()
            self.bird.draw()

            pygame.display.flip()
