"""
Single-pole balancing experiment using a feed-forward neural network.
"""

from __future__ import print_function

import multiprocessing
import os
import pickle

import neat

import visualize

import pygame
import numpy as np

from game_objects.ball import Ball
from game_objects.paddle import Paddle
from game_utils.utils import add_to_sprites_list


runs_per_net = 5
simulation_seconds = 25.0
framerate = 4000.0


# Use the NN network phenotype and the discrete actuator force function.
def eval_genome(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    miss = 0.0
    hits = 0.0
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    pygame.init()

    window_size = (700, 500)
    ball_radius = 20
    ball_velocity = 2
    display = pygame.display.set_mode(window_size)
    pygame.display.set_caption("neural pong")
    timer = pygame.time.Clock()

    for runs in range(runs_per_net):
        sim_time = 0.0
        paddle = Paddle(10, 100, WHITE, window_size[1])
        paddle.rect.x = 20
        paddle.rect.y = window_size[1]//2

        ball = Ball(ball_radius, ball_radius, WHITE, velocity = [ball_velocity,ball_velocity])
        ball.rect.x = window_size[0]//2
        ball.rect.y = window_size[1]//2

        sprites_list = pygame.sprite.Group()
        add_to_sprites_list(sprites_list, [paddle, ball])
        run = True

        # Run the given simulation for up to num_steps time steps.
        fitness = 0.0
        while sim_time < simulation_seconds and run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_x:
                        run = False

            inputs = [paddle.rect.y/window_size[1], ball.rect.y/window_size[1],
                      (ball.velocity[1]+ball_velocity)/(2*ball_velocity)]
            action = net.activate(inputs)
            # print("inputs",inputs)
            keys = pygame.key.get_pressed()
            # if np.argmax(action) == 0:
            #     paddle.move_up(5)
            # if np.argmax(action) == 1:
            #     paddle.move_down(5)

            if action[0] > 0.5:
                paddle.move_up(5)
            if action[0] <= 0.5:
                paddle.move_down(5)

            sprites_list.update()

            if ball.rect.x >= window_size[0] - ball_radius:
                ball.velocity[0] = -ball.velocity[0]
            if ball.rect.x <= 0:
                ball.rect.x = window_size[0] // 2
                ball.rect.y = window_size[1] // 2
                paddle.rect.x = 20
                paddle.rect.y = window_size[1] // 2
                miss += 1.0
                break
            if ball.rect.y > window_size[1] - ball_radius:
                ball.velocity[1] = -ball.velocity[1]
            if ball.rect.y < 0:
                ball.velocity[1] = -ball.velocity[1]

            if pygame.sprite.collide_mask(ball, paddle):
                ball.bounce()
                hits += 1.0

            display.fill(BLACK)
            sprites_list.draw(display)
            pygame.display.flip()

            timer.tick(int(framerate))
            sim_time += 1.0/framerate
        # print(fitness)
        # fitnesses.append(fitness)

    # The genome's fitness is its worst performance across all runs.
    return hits/(hits+miss) + sim_time


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = eval_genome(genome, config)


def run():
    # Load the config file, which is assumed to live in
    # the same directory as this script.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    pop = neat.Population(config)
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.StdOutReporter(True))

    pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), eval_genome)
    # pe = neat.ParallelEvaluator(1, eval_genome)
    winner = pop.run(pe.evaluate)

    # Save the winner.
    with open('winner-feedforward', 'wb') as f:
        pickle.dump(winner, f)

    print(winner)

    visualize.plot_stats(stats, ylog=True, view=True, filename="feedforward-fitness.svg")
    visualize.plot_species(stats, view=True, filename="feedforward-speciation.svg")

    node_names = {-1: 'paddle_y', -2: 'ball_y', -3: 'ball_dy', 0: 'control'}
    visualize.draw_net(config, winner, True, node_names=node_names)

    visualize.draw_net(config, winner, view=True, node_names=node_names,
                       filename="winner-feedforward.gv")
    # visualize.draw_net(config, winner, view=True, node_names=node_names,
    #                    filename="winner-feedforward-enabled.gv", show_disabled=False)
    # visualize.draw_net(config, winner, view=True, node_names=node_names,
    #                    filename="winner-feedforward-enabled-pruned.gv", show_disabled=False, prune_unused=True)


if __name__ == '__main__':
    run()