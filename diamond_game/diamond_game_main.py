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
#         self.rect = self.image.get_rect()
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
from weakref import WeakKeyDictionary
import pygame
from pygame.constants import DOUBLEBUF

from game_manager import *


class PygameView(EventManager):
    def __init__(self, ev_manager):
        EventManager.__init__(self)

        self.listeners = self.listeners
        self.dialog_listeners = WeakKeyDictionary()

        self.event_manager = ev_manager
        self.event_manager.register_listener(self)

        # load pygame modules
        pygame.init()
        # perform some set up
        # window caption
        pygame.display.set_caption("Chinese Checkers v 0.1")
        # size of window
        size = 400, 400  # size_x*Conf.piece_size, size_y*(Conf.piece_size+Conf.y_separation)
        # screen = pygame.display.set_mode(size, FULLSCREEN)  # make window
        self.screen = pygame.display.set_mode(size, DOUBLEBUF)  # make window and DOUBLEBUF for smooth animation
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

        self.dialog = None
        self.sub_views = []
        self.sprite_group = Group()

        self.view_classes = {'menu': [1], 'options': [1], 'main': [1]}
        # self.dialogClasses = {'msgDialog': BlockingDialogView}

        # the subviews that make up the current screen.  In order from
        # bottom to top
        # self.subviews = []
        self.switch_view('menu')

    def notify(self, event):
        if isinstance(event, TickEvent):
            # Draw Everything
            pass

    def switch_view(self, key):
        # if self.dialog:
        #     raise Exception('cannot switch view while dialog up')
        if not self.view_classes.has_key(key):
            raise NotImplementedError('master view doesnt have key')
        for view in self.sub_views:
            view.kill()
        self.sub_views = []
        self.sprite_group.empty()
        rect = pygame.Rect((0, 0), self.screen.get_size())
        # construct the new master View
        for view_class in self.view_classes[key]:
            if hasattr(view_class, 'clip_rect'):
                rect = view_class.clip_rect
            # view = view_class(self, self.sprite_group, rect)
            # bg_blit = view.GetBackgroundBlit()
            # self.background.blit(bg_blit[0], bg_blit[1])
            # self.sub_views.append(view)
        # initial blit & flip of the newly constructed background
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()


def main():
    event_manager = EventManager()
    controller = MasterController(event_manager)
    # keyboard = KeyboardController(event_manager)
    spinner = SpinnerController(event_manager)
    pygame_view = PygameView(event_manager)

    spinner.run()


if __name__ == "__main__":
    main()