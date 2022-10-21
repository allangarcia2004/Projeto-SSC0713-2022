import argparse

import pygame

from flappy_bird.gaming import Game

parser = argparse.ArgumentParser(description="FlappyBird Genético.")
parser.add_argument("--use-backup", action="store_true")
args = parser.parse_args()

pygame.init()
pygame.font.init()

game = Game(450, 800, args.use_backup)
game.run()
