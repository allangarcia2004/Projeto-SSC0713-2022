import sys
import pygame
import json
from evolution import Evolution

if len(sys.argv) == 2:
    arguments = json.loads(sys.argv[1])

    pygame.init()
    pygame.font.init()

    evolution = Evolution(
        use_backup=arguments['use_backup'],
        neurons_disposition=arguments['neurons_disposition'],
        population_size=arguments['population_size'],
        hall_of_fame_size=arguments['hall_of_fame_size'],
        tournament_size=arguments['tournament_size'],
        crossover_probability=arguments['crossover_probability'],
        mutation_probability=arguments['mutation_probability'],
        generations=arguments['generations'],
        fitness_weights=arguments['fitness_weights'],
        logbook_file=arguments['logbook_file']
    )

    evolution.run()

else:
    print("Argumentos inválidos!")
