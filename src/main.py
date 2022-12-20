import argparse
import pygame
from evolution import Evolution

parser = argparse.ArgumentParser(description="FlappyBird Genético.")
parser.add_argument("--use-backup", action="store_true")
args = parser.parse_args()

pygame.init()
pygame.font.init()

evolution = Evolution(use_backup=args.use_backup, neurons_disposition=[2, 3, 2],
                      population_size=900, hall_of_fame_size=20, tournament_size=90)

evolution.run(crossover_probability=0.3, mutation_probability=0.5,
              generations=100)
