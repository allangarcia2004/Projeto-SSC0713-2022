import pickle
from typing import List, Tuple, Sequence

import numpy as np
import pygame
from pygame import Vector2
from pygame.event import Event

from flappy_bird.gaming.bird import Bird, BirdSharedData
from flappy_bird.gaming.colors import Color
from flappy_bird.gaming.pipe import Pipe, PipeSharedData
from flappy_bird.gaming.world import WorldSharedData
from flappy_bird.neural_network import PlayersPopulation
from flappy_bird.neural_network.activation_functions import identity
from flappy_bird.neural_network.activation_functions import sigmoid


class Game:
    def __init__(self, screen_width: int, screen_height: int,
                 neurons_disposition: Sequence[int]):
        self.screen_size = Vector2(screen_width, screen_height)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.font = pygame.font.SysFont('Comic Sans MS', 30)

        self.closed = False
        self.clock = pygame.time.Clock()

        self.world_data = WorldSharedData(2.25, 5, self.screen_size, self.screen)
        self.bird_data = BirdSharedData(15.0, 21, 100, self.world_data)
        self.pipe_data = PipeSharedData(40, 140, self.world_data)

        self.players_population = PlayersPopulation(
            neurons_disposition, [identity, sigmoid]
        )

        self.pipe: Pipe = None
        self.bird_scores: List[int] = None
        self.bird = Bird(self.bird_data)
        self.bird.alive = True
        self.frames_loaded = 0
        self.pipes_bypassed = 0

        self.statistics_data = []
        self.wait_for_clock = False
        self.closed = False
        self.should_draw = True


    def render_text(self, text: str, position: Tuple[int, int]):
        text_surface = self.font.render(text, False, Color.WHITE, Color.BLACK)
        self.screen.blit(text_surface, position)

    def draw(self):
        self.screen.fill(Color.BLACK)
        self.bird.draw()
        self.pipe.draw()
        pygame.display.flip()

    def reset(self):
        self.frames_loaded = 0
        self.pipes_bypassed = 0
        self.bird = Bird(self.bird_data)
        self.pipe = Pipe(self.pipe_data)
        self.bird.alive = True

    def update(self, individual):
        neural_inputs = self.get_neural_inputs()

        if self.bird.alive:
            if self.bird.died_now(self.pipe):
                self.bird.alive = False
            elif self.pipe.frames_without_dashing > 50:
                self.bird.alive = False
            else:
                jump_decision, dash_value = self.players_population.should_move(individual, neural_inputs)
                if jump_decision:
                    self.bird.jump()
                self.pipe.dash(dash_value)
                self.frames_loaded += 1

        self.bird.update()
        self.pipe.update()

        if self.pipe.has_been_passed(self.bird):
            self.pipes_bypassed += 1



    def handle_event(self, event: Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_k:
                self.wait_for_clock = not self.wait_for_clock
            if event.key == pygame.K_d:
                self.should_draw = not self.should_draw

    def run(self, individual):
        self.reset()
        while not self.closed:

            for event in pygame.event.get():
                self.handle_event(event)

            if self.wait_for_clock:
                self.clock.tick(60)

            self.update(individual)

            if not self.bird.alive:
                return

            if self.should_draw:
                self.draw()

    def get_neural_input(self, bird: Bird):
        x = self.pipe.top_rect.left - bird.pos.x
        y = (self.pipe.top_rect.bottom + self.pipe.bottom_rect.top) / 2 - bird.pos.y
        return x, y

    def get_neural_inputs(self):
        return tuple(self.get_neural_input(self.bird))
