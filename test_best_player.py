"""
Test the performance of the best genome produced by evolve-feedforward.py.
"""

from __future__ import print_function

import os
import pickle

import pygame
import numpy as np

import neat

# load the winner
from game_objects.ball import Ball
from game_objects.paddle import Paddle
from game_utils.utils import add_to_sprites_list

with open('winner-feedforward_1', 'rb') as f:
    c = pickle.load(f)

print('Loaded genome:')
print(c)

# Load the config file, which is assumed to live in
# the same directory as this script.
local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'config-feedforward')
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     config_path)

net = neat.nn.FeedForwardNetwork.create(c, config)

simulation_seconds = 50
framerate = 60.0
miss = 0.0
hits = 0.0
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
pygame.init()

window_size = (700, 500)
ball_radius = 20
ball_velocity = 4
display = pygame.display.set_mode(window_size)
pygame.display.set_caption("neural pong")
timer = pygame.time.Clock()
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

    inputs = [paddle.rect.y / window_size[1], ball.rect.y / window_size[1],
              (ball.velocity[1] + ball_velocity) / (2 * ball_velocity)]
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


print('Agent played for {0:.1f} of {} seconds'.format(sim_time,simulation_seconds))