import pygame


class Paddle(pygame.sprite.Sprite):
    def __init__(self, width, height, color, window_height):
        super().__init__()
        self.BLACK = (0,0,0)

        self.color = color
        self.height = height
        self.window_height = window_height
        self.image = pygame.Surface([width, height])
        self.image.fill(self.BLACK)
        self.image.set_colorkey(self.BLACK)

        pygame.draw.rect(self.image, self.color, [0,0,width,height])

        self.rect = self.image.get_rect()

    def move_up(self, step):
        self.rect.y -= step
        if self.rect.y < 0:
            self.rect.y = 0

    def move_down(self, step):
        self.rect.y += step
        if self.rect.y > self.window_height-self.height:
            self.rect.y = self.window_height - self.height