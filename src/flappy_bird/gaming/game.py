from typing import List

import pygame
from pygame import Vector2
from pygame.event import Event

from flappy_bird.gaming.bird import BirdSharedData, Bird
from flappy_bird.gaming.colors import Color
from flappy_bird.gaming.pipe import PipeSharedData, Pipe
from flappy_bird.gaming.world import WorldSharedData
from flappy_bird.neural_network import PlayersPopulation
from flappy_bird.neural_network.activation_functions import identity


class Game:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_size = Vector2(screen_width, screen_height)
        self.screen = pygame.display.set_mode(self.screen_size)

        self.closed = False
        self.clock = pygame.time.Clock()

        self.birds_count = 1000

        self.world_data = WorldSharedData(2.25, 5, self.screen_size, self.screen)
        self.bird_data = BirdSharedData(15.0, 21, 100, self.world_data)
        self.pipe_data = PipeSharedData(40, 140, self.world_data)

        self.players_population = PlayersPopulation(
            self.birds_count, [2, 3, 1], [identity, identity]
        )

        self.alive_birds_count: int = None
        self.birds: List[Bird] = None
        self.pipe: Pipe = None
        self.bird_scores: List[int] = None

    def reset_generation(self):
        self.alive_birds_count = self.birds_count
        self.birds = [Bird(self.bird_data) for _ in range(self.birds_count)]
        self.pipe = Pipe(self.pipe_data)
        self.bird_scores = [0 for _ in range(self.birds_count)]

    def handle_event(self, event: Event):
        if event.type == pygame.QUIT:
            self.closed = True

    def update(self):
        neural_inputs = self.get_neural_inputs()
        self.players_population.feed_forward(neural_inputs)

        for index, bird in enumerate(self.birds):
            if bird.alive:
                if bird.died_now(self.pipe):
                    self.alive_birds_count -= 1
                else:
                    if self.players_population.should_jump(index):
                        bird.jump()
                    self.bird_scores[index] += 1
            bird.update()

        self.pipe.update()

    def draw(self):
        self.screen.fill(Color.BLACK)

        for bird in self.birds:
            bird.draw()

        self.pipe.draw()
        pygame.display.flip()

    def run_generation(self, draw: bool):
        while True:
            # self.clock.tick(60)
            for event in pygame.event.get():
                self.handle_event(event)

            self.update()
            if self.alive_birds_count == 0:
                return

            if draw:
                self.draw()

    def run(self):
        generation_count = 0
        while True:
            self.reset_generation()
            self.run_generation(True)
            self.players_population.evolution.set_fitnesses_on_individuals(self.bird_scores)
            self.players_population.evolution.run_generation()
            self.players_population.update_weights_and_biases_from_evolution()

            max_score = max(self.bird_scores)
            generation_count += 1
            print(f"Finished generation #{generation_count}. Max score: {max_score}")

    def get_neural_input(self, bird: Bird):
        x = self.pipe.top_rect.left - bird.pos.x
        y = (self.pipe.top_rect.bottom + self.pipe.bottom_rect.top) / 2 - bird.pos.y
        # z = bird.pos.y
        return x, y

    def get_neural_inputs(self):
        return tuple(map(self.get_neural_input, self.birds))
