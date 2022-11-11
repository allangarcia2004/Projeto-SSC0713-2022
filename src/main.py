import argparse

import pygame

from flappy_bird.evolution import Evolution

parser = argparse.ArgumentParser(description="FlappyBird Genético.")
parser.add_argument("--use-backup", action="store_true")
args = parser.parse_args()

pygame.init()
pygame.font.init()

evolution = Evolution(0.3, 0.3, args.use_backup, [2, 3, 1], 900)
evolution.run_generation()

