import pygame
import sys
from diamond_game.model.models import Board


def main():
    pygame.init()

    size = width, height = 320, 240
    speed = [2, 2]
    black = 0, 0, 0

    screen = pygame.display.set_mode(size)

    ball = pygame.image.load("test.png")
    ballrect = ball.get_rect()

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            ballrect = ballrect.move(speed)
            if ballrect.left < 0 or ballrect.right > width:
                speed[0] = -speed[0]
            if ballrect.top < 0 or ballrect.bottom > height:
                speed[1] = -speed[1]

            screen.fill(black)
            screen.blit(ball, ballrect)
            pygame.display.flip()


if __name__ == "__main__":
    x = 5
    for i in range(5):
        print 1
    board = Board()
    board.make_board()
    board.init_board()
    board.print_board()
    # main()