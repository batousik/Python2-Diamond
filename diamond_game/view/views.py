import pygame
from pygame.constants import DOUBLEBUF
from pygame.sprite import Group, Sprite
from diamond_game import *


class MVCView(MVCObject):
    def __init__(self, ev_manager):
        MVCObject.__init__(self, ev_manager)
        self.sprite_group = Group()
        self.images = {}
        self.background = pygame.Surface(Conf.screen_size)

    def get_image(self):
        self.sprite_group.update()
        self.sprite_group.draw(self.background)
        return self.background


class MasterView(MVCObject):
    def __init__(self, ev_manager):
        MVCObject.__init__(self, ev_manager)
        self.view_classes = {'menu': [MenuView], 'game': [GameView], 'options': [OptionsView]}
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
        elif isinstance(event, SwitchScreenEvent):
            self.switch_view(event.value)

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


class MenuView(MVCView):
    def __init__(self, ev_manager):
        MVCView.__init__(self, ev_manager)
        b1 = Button(Conf.green, Conf.b1_loc, (100, 20))
        b2 = Button(Conf.green, Conf.b2_loc, (100, 20))
        b3 = Button(Conf.green, Conf.b3_loc, (100, 20))
        b1.set_selected(1)
        self.buttons = [b1, b2, b3]
        self.sprite_group.add(b1, b2, b3)

    def notify(self, event):
        if isinstance(event, MenuSelectEvent):
            self.buttons[event.value].set_selected(1)
        elif isinstance(event, MenuUnSelectEvent):
            self.buttons[event.value].set_selected(0)
        elif isinstance(event, MouseMotionEvent):
            for i in range(0, len(self.buttons)):
                if self.buttons[i].rect.collidepoint(event.position):
                    self.post(ButtonHoverEvent(i))
                    break
        elif isinstance(event, MouseClickEvent):
            for i in range(0, len(self.buttons)):
                if self.buttons[i].rect.collidepoint(event.position):
                    self.post(MenuPressEvent())
                    break


class GameView(MVCView):
    def __init__(self, ev_manager):
        MVCView.__init__(self, ev_manager)
        self.fields = []
        self.pieces = []
        # Load images
        # Load sound

    def notify(self, event):
        if isinstance(event, BoardCreatedEvent):
            self.fields = event.value
        elif isinstance(event, PiecesCreatedEvent):
            self.pieces = event.value
            self.create_board()
            print "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        # if isinstance(event, MenuSelectEvent):
        #     self.buttons[event.value].set_selected(1)
        # elif isinstance(event, MenuUnSelectEvent):
        #     self.buttons[event.value].set_selected(0)
        # elif isinstance(event, MouseMotionEvent):
        #     for i in range(0, len(self.buttons)):
        #         if self.buttons[i].rect.collidepoint(event.position):
        #             self.post(ButtonHoverEvent(i))
        #             break
        # elif isinstance(event, MouseClickEvent):
        #     for i in range(0, len(self.buttons)):
        #         if self.buttons[i].rect.collidepoint(event.position):
        #             self.post(MenuPressEvent())
        #             break

    def create_board(self):
        for field in self.fields:
            loc = Conf.loc_to_view(field['x'], field['y'])
            piece = Field(field['val'], loc)
            self.sprite_group.add(piece)

    def create_pieces(self):
        for piece in self.pieces:
            loc = Conf.loc_to_view(piece['x'], piece['y'])
            piece = Piece(piece['val'], loc)
            self.sprite_group.add(piece)


class OptionsView(MVCView):
    def __init__(self, ev_manager):
        MVCView.__init__(self, ev_manager)
        self.fields = []
        self.pieces = []
        # Load images
        # Load sound

    def notify(self, event):
        pass
        # if isinstance(event, BoardCreatedEvent):
        #     self.fields = event.value
        # elif isinstance(event, PiecesCreatedEvent):
        #     self.pieces = event.value
        #     self.create_board()
        # if isinstance(event, MenuSelectEvent):
        #     self.buttons[event.value].set_selected(1)
        # elif isinstance(event, MenuUnSelectEvent):
        #     self.buttons[event.value].set_selected(0)
        # elif isinstance(event, MouseMotionEvent):
        #     for i in range(0, len(self.buttons)):
        #         if self.buttons[i].rect.collidepoint(event.position):
        #             self.post(ButtonHoverEvent(i))
        #             break
        # elif isinstance(event, MouseClickEvent):
        #     for i in range(0, len(self.buttons)):
        #         if self.buttons[i].rect.collidepoint(event.position):
        #             self.post(MenuPressEvent())
        #             break


class Piece(Sprite):
    def __init__(self, player, loc):
        Sprite.__init__(self)
        self.image = pygame.Surface([Conf.piece_size, Conf.piece_size])
        self.image.fill(Conf.colours[player])
        self.rect = self.image.get_rect()
        self.rect.center = loc
        self.dragged = False

    def is_clicked(self):
        return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos())

    def update(self):
        """
        :return:perform sprite update
        """

        if self.dragged:
            pos = pygame.mouse.get_pos()
            self.rect.center = pos
            self.dragged = pygame.mouse.get_pressed()[0]
        else:
            self.dragged = self.is_clicked()


class Field(Sprite):
    def __init__(self, field_type, loc):
        Sprite.__init__(self)
        self.image = pygame.Surface([Conf.piece_size, Conf.piece_size])
        self.image.fill(Conf.colours[field_type])
        self.rect = self.image.get_rect()
        self.rect.center = loc


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


if __name__ == "__main__":
    raise Exception("Unexpected")
