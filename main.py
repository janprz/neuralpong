import pygame

from game_objects.ball import Ball
from game_objects.paddle import Paddle
from game_utils.utils import add_to_sprites_list

if __name__ == '__main__':
    WHITE = (255,255,255)
    BLACK = (0,0,0)
    pygame.init()

    window_size = (700,500)
    ball_radius = 20
    display = pygame.display.set_mode(window_size)
    pygame.display.set_caption("neural pong")

    paddleA = Paddle(10, 100, WHITE, window_size[1])
    paddleA.rect.x = 20
    paddleA.rect.y = 200

    ball = Ball(ball_radius,ball_radius,WHITE)
    ball.rect.x = 100
    ball.rect.y = 100

    sprites_list = pygame.sprite.Group()
    add_to_sprites_list(sprites_list, [paddleA, ball])
    run = True

    timer = pygame.time.Clock()

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            paddleA.move_up(5)
        if keys[pygame.K_s]:
            paddleA.move_down(5)

        sprites_list.update()

        if ball.rect.x >= window_size[0]-ball_radius:
            ball.velocity[0] = -ball.velocity[0]
        if ball.rect.x <= 0:
            ball.velocity[0] = -ball.velocity[0]
        if ball.rect.y > window_size[1]-ball_radius:
            ball.velocity[1] = -ball.velocity[1]
        if ball.rect.y < 0:
            ball.velocity[1] = -ball.velocity[1]

        if pygame.sprite.collide_mask(ball, paddleA) :
            ball.bounce()

        display.fill(BLACK)
        sprites_list.draw(display)
        pygame.display.flip()

        timer.tick(60)

    pygame.quit()


