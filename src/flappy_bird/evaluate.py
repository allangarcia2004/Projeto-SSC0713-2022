from flappy_bird.gaming import Game


class Evaluate:
    def __init__(self, neurons_disposition):
        self.game = Game(450, 800, neurons_disposition)

    def run(self, individual):
        self.game.run(individual)

        return self.game.score,
