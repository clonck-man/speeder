import neat
import pygame

from car_game_engine.car_game import Game


generation = 0


def compute_fitness(vitesse, vitesse_max, checkpoints_valides):
    poids_vitesse = 0.1
    poids_checkpoints = 1.0

    fitness = (poids_vitesse * vitesse/vitesse_max) + (poids_checkpoints * checkpoints_valides)
    return fitness


def eval_genome(genome_id, genome):
    global generation

    net = neat.nn.FeedForwardNetwork.create(genome, config)

    game = Game()
    fitness = 0
    ck = 0

    not_moving = 0
    nb_frames = 0
    while not game.victory and not game.crash:
        dt = game.clock.get_time() / 1000

        inputs = [game.car.angle, game.car.velocity]
        inputs.extend(game.car.get_view(game.walls, return_dist=True))

        outputs = [output > 0 for output in net.activate(inputs)]
        game.logic_blind(dt, outputs)

        if game.car.velocity == 0:
            not_moving += 1

        if not_moving > 10:
            break

        game.add_to_board("generation", generation)
        game.add_to_board("genome_id", genome_id)

        game.draw()
        game.display_board()
        pygame.display.flip()

        fitness += compute_fitness(game.car.velocity, game.car.max_velocity, len(game.validated_checkpoints) - ck)
        ck = len(game.validated_checkpoints)

        game.clock.tick(game.ticks)

        nb_frames += 1

    if game.victory:
        fitness += (1 / nb_frames) * 1000

    genome.fitness = fitness


def eval_genomes(genomes, config):
    global generation

    for genome_id, genome in genomes:
        eval_genome(genome_id, genome)
    generation += 1


config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     'config.txt')

p = neat.Population(config)
p.add_reporter(neat.StdOutReporter(True))
stats = neat.StatisticsReporter()
p.add_reporter(stats)
p.run(eval_genomes, 50)
