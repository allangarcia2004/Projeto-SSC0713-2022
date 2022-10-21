import pickle
from typing import List, Tuple

import keyboard
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


class Game:
    def __init__(self, screen_width: int, screen_height: int, use_backup: bool):
        self.screen_size = Vector2(screen_width, screen_height)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.font = pygame.font.SysFont('Comic Sans MS', 30)

        self.closed = False
        self.clock = pygame.time.Clock()

        self.birds_count = 900

        self.world_data = WorldSharedData(2.25, 5, self.screen_size, self.screen)
        self.bird_data = BirdSharedData(15.0, 21, 100, self.world_data)
        self.pipe_data = PipeSharedData(40, 140, self.world_data)

        self.players_population = PlayersPopulation(
            self.birds_count, [2, 3, 1], [identity, identity], use_backup=use_backup
        )

        self.alive_birds_count: int = None
        self.max_score: int = None
        self.max_pipes_bypassed: int = None
        self.birds: List[Bird] = None
        self.pipe: Pipe = None
        self.bird_scores: List[int] = None

        self.statistics_data = []
        self.wait_for_clock = False
        self.closed = False
        self.should_draw = True

        keyboard.add_hotkey("k", self.toggle_wait_for_clock)
        keyboard.add_hotkey("q", self.close)
        keyboard.add_hotkey("d", self.toggle_draw)

    def toggle_draw(self):
        self.should_draw = not self.should_draw

    def close(self):
        self.closed = True

    def toggle_wait_for_clock(self):
        self.wait_for_clock = not self.wait_for_clock

    def reset_generation(self):
        self.alive_birds_count = self.birds_count
        self.max_score = 0
        self.max_pipes_bypassed = 0
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
                    self.max_score = max(self.max_score, self.bird_scores[index])
            bird.update()

        if self.pipe.x_pos == self.pipe.initial_position:
            self.max_pipes_bypassed += 1
        self.pipe.update()

    def render_text(self, text: str, position: Tuple[int, int]):
        text_surface = self.font.render(text, False, Color.WHITE, Color.BLACK)
        self.screen.blit(text_surface, position)

    def draw(self):
        self.screen.fill(Color.BLACK)

        for bird in self.birds:
            bird.draw()

        self.pipe.draw()

        self.render_text(f"Max Score: {self.max_score}", (10, 10))
        self.render_text(f"Max Pipes Bypassed: {self.max_pipes_bypassed}", (10, 40))
        self.render_text(f"Birds Alive: {self.alive_birds_count}", (10, 70))

        pygame.display.flip()

    def run_generation(self):
        while not self.closed:
            if self.wait_for_clock:
                self.clock.tick(60)
            for event in pygame.event.get():
                self.handle_event(event)

            self.update()
            if self.alive_birds_count == 0:
                return

            if self.should_draw:
                self.draw()

    def run(self):
        generation_count = 0
        while not self.closed:
            self.reset_generation()
            self.run_generation()

            self.players_population.evolution.set_fitnesses_on_individuals(self.bird_scores)
            self.players_population.evolution.run_generation()
            self.players_population.update_weights_and_biases_from_evolution()

            generation_data = {
                "median": np.median(self.bird_scores), "average": np.average(self.bird_scores),
                "std": np.std(self.bird_scores), "max": np.max(self.bird_scores), "min": np.min(self.bird_scores)
            }
            self.statistics_data.append(generation_data)

            max_score = max(self.bird_scores)
            generation_count += 1
            print(f"Finished generation #{generation_count}. Max score: {max_score}")

        with open("statistics_by_generation.pickle", "wb") as file:
            pickle.dump(self.statistics_data, file)

    def get_neural_input(self, bird: Bird):
        x = self.pipe.top_rect.left - bird.pos.x
        y = (self.pipe.top_rect.bottom + self.pipe.bottom_rect.top) / 2 - bird.pos.y
        return x, y

    def get_neural_inputs(self):
        return tuple(map(self.get_neural_input, self.birds))
