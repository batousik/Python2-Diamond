import os
import pygame
import sys
from diamond_game.model.models import Board
import Queue

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

a = Queue.Queue(0)
a.put(1)
a.put(1)
a.put(1)
a.put(1)

def geta():
    if not a.empty():
        return a.get()


if __name__ == "__main__":
    x = 5
    for i in range(5):
        print 1
    board = Board()
    board.make_board()
    board.init_board()
    board.print_board()
    print -x
    for file in os.listdir("sounds"):
        fullname = os.path.join('sounds', file)
        print fullname

    event = geta()
    print event
    while event is not None:
        print event
        event = geta()

    # main()