import sys
import pygame
from pygame.sprite import Group
from diamond_game import Conf
from diamond_game.model import Model


"""
This module has a main procedure that prints "Hello Diamond"
Then starts small pygame example
"""


class Piece(pygame.sprite.Sprite):
    def __init__(self, color, loc):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([Conf.piece_size, Conf.piece_size])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = loc


def main():

    model = Model()
    model.init_game([], [1, 2, 3, 4])
    size_x, size_y = model.get_grid_dimensions()
    print Conf.y_separation
    pygame.init()  # load pygame modules
    size = size_x*Conf.piece_size, size_y*(Conf.piece_size+Conf.y_separation)  # size of window
    screen = pygame.display.set_mode(size)  # make window

    all_sprites_list = Group()

    # draw board
    for field in model.get_board_grid():
        loc = Conf.loc_to_view(field['x'], field['y'])
        pygame.draw.circle(screen, Conf.colours[field['val']], loc, Conf.piece_rad, 0)

    # create pieces sprites
    for piece in model.get_pieces():
        loc = Conf.loc_to_view(piece['x'], piece['y'])
        color = Conf.colours[piece['val']]
        p = Piece(color, loc)
        all_sprites_list.add(p)

    clock = pygame.time.Clock()  # make a clock
    while 1:  # infinite loop
        all_sprites_list.draw(screen)
        pygame.display.update()
        clock.tick(100)  # limit framerate to 100 FPS
        for event in pygame.event.get():  # if something clicked
                if event.type == pygame.QUIT:  # if EXIT clicked
                        sys.exit()  # close cleanly
        pygame.display.flip()  # update the screen


if __name__ == "__main__":
    print("Hello Diamond")
    main()
