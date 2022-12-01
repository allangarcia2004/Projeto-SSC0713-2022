import pygame
from flappy_bird.gaming.game import Game
from pygame.event import Event
from typing import Sequence


class Evaluate:
    def __init__(self, population, neurons_disposition: Sequence[int],
                 population_size: int):
        self.game = Game(450, 800, population, population_size, neurons_disposition)

    def handle_event(self, event: Event):
        if event.type == pygame.QUIT:
            self.game.closed = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.game.closed = True
            if event.key == pygame.K_k:
                self.game.wait_for_clock = not self.game.wait_for_clock
            if event.key == pygame.K_d:
                self.game.should_draw = not self.game.should_draw

    def run(self, population: list):

        for event in pygame.event.get():
            self.handle_event(event)

        self.game.run(population)

        fitnesses = []
        for fitness_value in self.game.bird_scores:
            fitnesses.append( (fitness_value,) )

        return fitnesses

