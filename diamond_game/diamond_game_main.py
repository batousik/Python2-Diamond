# -*- coding: utf-8 -*-
# import sys
# import os
# from pygame.constants import RLEACCEL
from pygame.sprite import Group
from diamond_game.controller.controllers import SpinnerController, MasterController
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
# class Piece(pygame.sprite.Sprite):
#     def __init__(self, colour, loc):
#         pygame.sprite.Sprite.__init__(self)
#         self.image = pygame.Surface([Conf.piece_size, Conf.piece_size])
#         self.image.fill(colour)
#         self.rect = self.image.get_rect() lj b
#         self.rect.center = loc
#         self.dragged = False
#
#     def is_clicked(self):
#         return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos())
#
#     def update(self):
#         """
#         :return:perform sprite update
#         """
#
#         if self.dragged:
#             pos = pygame.mouse.get_pos()
#             self.rect.center = pos
#             self.dragged = pygame.mouse.get_pressed()[0]
#         else:
#             self.dragged = self.is_clicked()
#
# # def load_image(name, colorkey=None):
# #     fullname = os.path.join('data', name)
# #     try:
# #         image = pygame.image.load(fullname)
# #     except pygame.error, message:
# #         print 'Cannot load image:', name
# #         raise SystemExit, message
# #     image = image.convert()
# #     if colorkey is not None:
# #         if colorkey is -1:
# #             colorkey = image.get_at((0, 0))
# #         image.set_colorkey(colorkey, RLEACCEL)
# #     return image, image.get_rect()
# #
# #
# # def load_sound(name):
# #     class NoneSound:
# #         def play(self): pass
# #     if not pygame.mixer:
# #         return NoneSound()
# #     fullname = os.path.join('data', name)
# #     try:
# #         sound = pygame.mixer.Sound(fullname)
# #     except pygame.error, message:
# #         print 'Cannot load sound:', wav
# #         raise SystemExit, message
# #     return sound
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
from diamond_game.model.models import MasterModel
from diamond_game.view.views import MasterView
from diamond_game import *





def main():
    event_manager = EventManager()
    model = MasterModel(event_manager)
    controller = MasterController(event_manager)
    # keyboard = KeyboardController(event_manager)
    spinner = SpinnerController(event_manager)
    pygame_view = MasterView(event_manager)

    spinner.run()


if __name__ == "__main__":
    main()