import pygame

from .bird import Bird
from .colors import Color


class Game:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_size = (screen_width, screen_height)
        self.screen = pygame.display.set_mode(self.screen_size)

        self.closed = False
        self.clock = pygame.time.Clock()

        self.bird = Bird(self.screen, 15, (30, screen_height // 2))

    def run(self):
        while not self.closed:
            self.clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.closed = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.bird.jump()

            self.screen.fill(Color.BLACK)

            self.bird.update()
            self.bird.draw()

            pygame.display.flip()
