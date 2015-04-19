import pygame
from pygame.constants import DOUBLEBUF
from pygame.sprite import DirtySprite, LayeredDirty
from diamond_game import *


class MVCView(MVCObject):
    def __init__(self, ev_manager, name):
        MVCObject.__init__(self, ev_manager, name)
        self.sprite_group = LayeredDirty()
        self.images = {}
        self.background = pygame.Surface(Conf.screen_size)

    def get_image(self):
        self.sprite_group.update()
        self.sprite_group.draw(self.background)
        return self.background


class MasterView(MVCObject):
    def __init__(self, ev_manager):
        MVCObject.__init__(self, ev_manager, '[view]')
        self.id = Conf.VIEW
        self.event_manager = ev_manager
        self.sub_classes = {Conf.MENU: [MenuView],
                            Conf.GAME: [GameView],
                            Conf.OPTIONS: [OptionsView]}

        # perform some set up
        # window caption
        pygame.display.set_caption("Chinese Checkers v 0.2")
        # screen = pygame.display.set_mode(size, FULLSCREEN)  # make window
        # make window and DOUBLEBUF for smooth animation
        self.screen = pygame.display.set_mode(Conf.screen_size, DOUBLEBUF)
        self.background = pygame.Surface(Conf.screen_size)
        # transfer background
        self.screen.blit(self.background, (0, 0))
        # update screen
        pygame.display.flip()
        # First view is menu
        self.switch_sub_modules(Conf.MENU)

    def get_next_event(self):
        return self.event_manager.get_next_view_event()

    # def switch_sub_modules(self, key):
    #     self.sub_modules = []
    #     for a_view in self.sub_classes[key]:
    #         new_view = a_view(self.event_manager)
    #         bg = new_view.get_image()
    #         self.background.blit(bg, (0, 0))
    #         self.sub_modules.append(new_view)
    #     # initial blit & flip of the newly constructed background
    #     self.screen.blit(self.background, (0, 0))
    #     pygame.display.flip()

    def run(self):
        running = 1
        while running:
            event = self.get_next_event()
            if isinstance(event, QuitEvent):
                # Terminate view thread
                print self.thread_name + ' is shutting down'
                running = 0
            elif isinstance(event, TickEvent):
                # Update view according to FPS
                for a_view in self.sub_modules:
                    view_bg = a_view.get_image()
                    self.background.blit(view_bg, (0, 0))
                self.screen.blit(self.background, (0, 0))
                pygame.display.flip()
            elif isinstance(event, SwitchScreenEvent):
                self.switch_sub_modules(event.value)
            else:
                for a_view in self.sub_modules:
                    if a_view.does_handle_event(event):
                        a_view.handle_event(event)


class MenuView(MVCView):
    def __init__(self, ev_manager):
        MVCView.__init__(self, ev_manager, '[MenuView]')
        b1 = Button(Conf.green, Conf.b1_loc, (100, 20))
        b2 = Button(Conf.green, Conf.b2_loc, (100, 20))
        b3 = Button(Conf.green, Conf.b3_loc, (100, 20))
        b1.set_selected(1)
        self.buttons = [b1, b2, b3]
        self.sprite_group.add(b1, b2, b3)

    def does_handle_event(self, event):
        return 1

    def handle_event(self, event):
        if isinstance(event, MenuSelectEvent):
            self.buttons[event.value].set_selected(1)
        elif isinstance(event, MenuUnSelectEvent):
            self.buttons[event.value].set_selected(0)
        elif isinstance(event, MouseMotionEvent):
            for i in range(0, len(self.buttons)):
                if self.buttons[i].rect.collidepoint(event.position):
                    self.post(ButtonHoverEvent(i), Conf.MODEL)
                    break
        elif isinstance(event, MouseClickEvent):
            for i in range(0, len(self.buttons)):
                if self.buttons[i].rect.collidepoint(event.position):
                    self.post(MenuPressEvent(), Conf.MODEL)
                    break


class GameView(MVCView):
    def __init__(self, ev_manager):
        MVCView.__init__(self, ev_manager, '[GameView]')
        self.fields_start_locs = []
        self.pieces_start_locs = []
        # list of pieces sprites
        self.pieces = []
        self.click_sprites = LayeredDirty()
        # Load images
        # Load sound

    def does_handle_event(self, event):
        return 1

    def handle_event(self, event):
        if isinstance(event, BoardCreatedEvent):
            self.fields_start_locs = event.value
            self.create_board()
        elif isinstance(event, PiecesCreatedEvent):
            self.pieces_start_locs = event.value
            self.create_pieces()
        elif isinstance(event, PieceMoveEvent):
            # get piece at self start
            # move to self end
            self.move_piece(event.start, event.end)
        elif isinstance(event, MouseClickEvent):
            for sprite in self.click_sprites:
                if sprite.rect.collidepoint(event.position):
                    x, y = (event.position[0], event.position[1])
                    self.post(
                        GameObjectClickEvent(Conf.GAME_PLAY, Conf.loc_to_model(x, y)),
                        Conf.MODEL)
                    break

        # if isinstance(event, MenuSelectEvent):
        #     self.buttons[event.value].set_selected(1)
        # elif isinstance(event, MenuUnSelectEvent):
        #     self.buttons[event.value].set_selected(0)
        # elif isinstance(event, MouseMotionEvent):
        #     for i in range(0, len(self.buttons)):
        #         if self.buttons[i].rect.collidepoint(event.position):
        #             self.post(ButtonHoverEvent(i))
        #             break

    def create_board(self):
        for field in self.fields_start_locs:
            loc = Conf.loc_to_view(field['x'], field['y'])
            new_field = Field(field['val'], loc)
            self.sprite_group.add(new_field)
            self.click_sprites.add(new_field)

    def create_pieces(self):
        for piece in self.pieces_start_locs:
            loc = Conf.loc_to_view(piece['x'], piece['y'])
            new_piece = Piece(piece['val'], loc)
            self.click_sprites.add(new_piece)
            self.sprite_group.add(new_piece)
            self.pieces.append(new_piece)

    def move_piece(self, start, end):
        piece = self.get_piece(start)
        piece.set_new_loc(end)

    def get_piece(self, loc):
        view_loc = Conf.loc_to_view(loc[0], loc[1])
        for piece in self.pieces:
            if piece.is_collided(view_loc):
                return piece


class OptionsView(MVCView):
    def __init__(self, ev_manager):
        MVCView.__init__(self, ev_manager)
        self.fields = []
        self.pieces = []
        # Load images
        # Load sound


class Piece(DirtySprite):
    def __init__(self, player, loc):
        DirtySprite.__init__(self)
        self.image = pygame.Surface([Conf.piece_size, Conf.piece_size])
        self.image.fill(Conf.colours[player])
        self.rect = self.image.get_rect()
        self.rect.center = loc
        self.new_loc = loc
        self.player = player
        self.selected = 0
        self.dirty = 2
        # self.dragged = False

    def is_collided(self, view_loc):
        return self.rect.collidepoint(view_loc)

    def set_new_loc(self, loc):
        self.new_loc = Conf.loc_to_view(loc[0], loc[1])

    def update(self):
        if self.selected:
            self.image.fill(Conf.black)
        else:
            self.image.fill(Conf.colours[self.player])
        if not self.rect.center == self.new_loc:
            x, y = self.rect.center
            new_x, new_y = self.new_loc
            dx = 0
            dy = 0
            if x < new_x:
                dx = 1
            elif x > new_x:
                dx = -1
            if y < new_y:
                dy = 1
            elif y > new_y:
                dy = -1
            self.rect.center = (x + dx, y + dy)


class Field(DirtySprite):
    def __init__(self, field_type, loc):
        DirtySprite.__init__(self)
        self.image = pygame.Surface([Conf.piece_size, Conf.piece_size])
        self.image.fill(Conf.colours[field_type])
        self.rect = self.image.get_rect()
        self.rect.center = loc
        self.dirty = 2


class Button(DirtySprite):
    def __init__(self, colour, loc, size):
        DirtySprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.center = loc
        self.selected = 0
        self.dirty = 2

    def set_selected(self, val):
        self.selected = val

    def update(self):
        if self.selected:
            self.image.fill((100, 100, 100))
        else:
            self.image.fill((200, 200, 200))


if __name__ == "__main__":
    raise Exception("Unexpected")
