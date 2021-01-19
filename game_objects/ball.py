import pygame
from random import randint
import numpy as np
BLACK = (0,0,0)

class Ball(pygame.sprite.Sprite):

    def __init__(self, width, height, color, velocity = [2,2]):
        super().__init__()

        self.velocity = velocity
        self.image = pygame.Surface([ width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def bounce(self):
        self.velocity[0] = -self.velocity[0]
        # self.velocity[1] = self.velocity[1]
        self.velocity[1] = randint(self.velocity[0], -self.velocity[0]) if self.velocity[0] < 0 else randint(-self.velocity[0], self.velocity[0])