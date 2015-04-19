# -*- coding: utf-8 -*-
# import sys
# import os
# from pygame.constants import RLEACCEL
#
# # check for sound and fonts support
# if not pygame.font:
#     print 'Warning, fonts disabled'
# if not pygame.mixer:
#     print 'Warning, sound disabled'
#
# """
# This module has a main procedure that prints "Hello Diamond"
# Then starts small pygame example
# """
#
#

#
# #
#
#
# class View(object):
#     def __init__(self):
#         pass
#
#     def draw_board(self):
#         pass
#
#
# def main():
#
#     model = Model()
#     model.init_game([], [1, 2, 3, 4])
#     size_x, size_y = model.get_grid_dimensions()
#     print Conf.y_separation
#     pygame.init()  # load pygame modules
#     # perform some set up
#     pygame.display.set_caption("Alalala")  # window caption
#     size = size_x*Conf.piece_size, size_y*(Conf.piece_size+Conf.y_separation)  # size of window
#     # screen = pygame.display.set_mode(size, FULLSCREEN)  # make window
#     screen = pygame.display.set_mode(size, DOUBLEBUF)  # make window and DOUBLEBUF for smooth animation
#     # extend to PyOpenGL?
#
#     all_sprites_list = Group()
#
#     # draw board
#     for field in model.get_board_grid():
#         loc = Conf.loc_to_view(field['x'], field['y'])
#         pygame.draw.circle(screen, Conf.colours[field['val']], loc, Conf.piece_rad, 0)
#
#     # create pieces sprites
#     for piece in model.get_pieces():
#         loc = Conf.loc_to_view(piece['x'], piece['y'])
#         colour = Conf.colours[piece['val']]
#         p = Piece(colour, loc)
#         all_sprites_list.add(p)
#
#     clock = pygame.time.Clock()  # make a clock
#     while 1:  # infinite loop
#         clock.tick(100)  # limit framerate to 100 FPS
#         for event in pygame.event.get():  # if something clicked
#                 if event.type == pygame.QUIT:  # if EXIT clicked
#                         sys.exit()  # close cleanly
#         # RENDERING
#
#         # need background
#         # background = pygame.image.load('track.png')
#         # screen.blit(self.background, (0,0))
#         screen.fill((0, 0, 0))
#         # need board to be drawn different way
#         for field in model.get_board_grid():
#             loc = Conf.loc_to_view(field['x'], field['y'])
#             pygame.draw.circle(screen, Conf.colours[field['val']], loc, Conf.piece_rad, 0)
#         all_sprites_list.update()
#         all_sprites_list.draw(screen)
#         pygame.display.flip()  # update the screen
#
#
# if __name__ == "__main__":
#     print("Hello Diamond")
#     main()
import pygame
import time
from diamond_game import *


def main():
    # load pygame modules
    pygame.init()
    event_manager = EventManager()

    controller_thread = MasterControllerThreaded(event_manager)
    view_thread = MasterViewThreaded(event_manager)
    model_thread = MasterModelThreaded(event_manager)

    view_thread.start()
    model_thread.start()
    controller_thread.start()

    while controller_thread.is_alive() or view_thread.is_alive() \
            or model_thread.is_alive():
        time.sleep(0.01)
        event_manager.post(TickEvent(), Conf.VIEW)
        pygame.event.pump()

    print '_____END_____'

if __name__ == "__main__":
    main()