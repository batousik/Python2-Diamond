import pygame
from pygame.constants import DOUBLEBUF
from pygame.sprite import Group, Sprite
from diamond_game import *


class MasterView(MVCObject):
    def __init__(self, ev_manager):
        MVCObject.__init__(self, ev_manager)
        self.view_classes = {'menu': [MenuView], 'options': [1], 'main': [1]}
        self.sub_views = []

        # load pygame modules
        pygame.init()
        # perform some set up
        # window caption
        pygame.display.set_caption("Chinese Checkers v 0.1")
        # screen = pygame.display.set_mode(size, FULLSCREEN)  # make window
        # make window and DOUBLEBUF for smooth animation
        self.screen = pygame.display.set_mode(Conf.screen_size, DOUBLEBUF)
        self.background = pygame.Surface(Conf.screen_size)
        # transfer background
        self.screen.blit(self.background, (0, 0))
        # update screen
        pygame.display.flip()
        # First view is menu
        self.switch_view('menu')

    def notify(self, event):
        if isinstance(event, TickEvent):
            for view in self.sub_views:
                view_bg = view.get_image()
                self.background.blit(view_bg, (0, 0))
            self.screen.blit(self.background, (0, 0))
            pygame.display.flip()

    def switch_view(self, key):
        self.sub_views = []
        # construct the new View
        for view in self.view_classes[key]:
            new_view = view(self.event_manager)
            bg = new_view.get_image()
            self.background.blit(bg, (0, 0))
            self.sub_views.append(new_view)
        # initial blit & flip of the newly constructed background
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()


class MenuView(MVCObject):
    def __init__(self, ev_manager):
        MVCObject.__init__(self, ev_manager)
        self.sprite_group = Group()
        self.background = pygame.Surface(Conf.screen_size)
        b1 = Button(Conf.green, Conf.b1_loc, (100, 20))
        b2 = Button(Conf.green, Conf.b2_loc, (100, 20))
        b3 = Button(Conf.green, Conf.b3_loc, (100, 20))
        b1.set_selected(1)
        self.buttons = [b1, b2, b3]
        self.sprite_group.add(b1, b2, b3)

    def get_image(self):
        self.sprite_group.update()
        self.sprite_group.draw(self.background)
        return self.background

    def notify(self, event):
        if isinstance(event, MenuSelectEvent):
            self.buttons[event.value].set_selected(1)
        elif isinstance(event, MenuUnSelectEvent):
            self.buttons[event.value].set_selected(0)
        elif isinstance(event, MenuMouseMotionEvent):
            for s in 0..len(self.buttons):
                if self.buttons[s].rect.collidepoint(event.position):
                    self.post(MenuMouseHoverEvent(s))
                    break
        elif isinstance(event, MenuMouseClickEvent):
            for s in 0..len(self.buttons):
                if self.buttons[s].rect.collidepoint(event.position):
                    self.post(MenuMouseHoverEvent(s))
                    break


class Button(Sprite):
    def __init__(self, colour, loc, size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.center = loc
        self.selected = 0

    def set_selected(self, val):
        self.selected = val

    def update(self):
        if self.selected:
            self.image.fill((100, 100, 100))
        else:
            self.image.fill((200, 200, 200))
