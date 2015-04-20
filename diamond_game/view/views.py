import pygame
from pygame.constants import DOUBLEBUF
from pygame.sprite import DirtySprite, LayeredDirty
import sys
from diamond_game import *
import time


class MVCView(MVCObject):
    def __init__(self, ev_manager, name):
        MVCObject.__init__(self, ev_manager, name)
        self.sprite_group = LayeredDirty()
        self.images = {}
        self.background = pygame.Surface(Conf.SCREEN_SIZE)
        self.background_sprite = BackGround()
        self.sprite_group.add(self.background_sprite)

    def get_image(self):
        self.background = pygame.Surface(Conf.SCREEN_SIZE)
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
        self.screen = pygame.display.set_mode(Conf.SCREEN_SIZE, DOUBLEBUF)
        self.background_sprite = BackGround()
        self.background = pygame.Surface(Conf.SCREEN_SIZE)
        self.background.blit(self.background_sprite.image, self.background_sprite.rect)
        # transfer background
        self.screen.blit(self.background, (0, 0))
        # update screen
        pygame.display.flip()
        # First view is menu
        time.sleep(1)
        self.switch_sub_modules(Conf.MENU)

    @property
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

    # noinspection PyBroadException
    def run(self):
        running = 1
        try:
            while running:
                event = self.get_next_event
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
        except:
            e = sys.exc_info()[0]
            print '>>>>>>>>>>> Fatal Error in: ' + self.thread_name
            print e
            self.post(QuitEvent(), Conf.ALL)


class MenuView(MVCView):
    def __init__(self, ev_manager):
        MVCView.__init__(self, ev_manager, '[MenuView]')
        b1 = Button(Conf.B1_LOC, (Utils.load_image('b1_u'), Utils.load_image('b1_s')))
        b2 = Button(Conf.B2_LOC, (Utils.load_image('b2_u'), Utils.load_image('b2_s')))
        b3 = Button(Conf.B3_LOC, (Utils.load_image('b3_u'), Utils.load_image('b3_s')))
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
                    self.post(SoundPlayEvent('menu_click'), Conf.SOUND)
                    self.post(MenuPressEvent(), Conf.MODEL)
                    break


class GameView(MVCView):
    def __init__(self, ev_manager):
        MVCView.__init__(self, ev_manager, '[GameView]')
        self.fields_start_locs = []
        self.pieces_start_locs = []
        # list of pieces sprites
        self.pieces = []
        self.fields = []
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
            # get piece by uid
            # move to new location
            self.move_piece(event.start, event.end)
        elif isinstance(event, PieceSelectedEvent):
            self.post(SoundPlayEvent('select'), Conf.SOUND)
            self.set_piece_selected(event.value, 1)
        elif isinstance(event, PieceDeSelectedEvent):
            self.post(SoundPlayEvent('deselect'), Conf.SOUND)
            self.set_piece_selected(event.value, 0)
        elif isinstance(event, CreateAvailableLocs):
            self.set_available_locs(event.locs, 1)
        elif isinstance(event, RemoveAvailableLocs):
            self.set_available_locs(event.locs, 0)
        elif isinstance(event, MouseClickEvent):
            for sprite in self.click_sprites:
                if sprite.rect.collidepoint(event.position):
                    x, y = (event.position[0], event.position[1])
                    self.post(
                        GameObjectClickEvent(Conf.GAME_PLAY, Conf.loc_to_model(x, y)),
                        Conf.MODEL)
                    break

    def create_board(self):
        """
        Create Field sprites, with colour (empty)
        from list of received locations
        """
        for field in self.fields_start_locs:
            loc = Conf.loc_to_view(field[0], field[1])
            new_field = Field(Conf.EMPTY, loc)
            self.sprite_group.add(new_field)
            self.click_sprites.add(new_field)
            self.fields.append(new_field)

    def create_pieces(self):
        self.pieces = []
        for piece in self.pieces_start_locs:
            loc = Conf.loc_to_view(piece['x'], piece['y'])
            new_piece = Piece(piece['piece'], loc)
            self.click_sprites.add(new_piece)
            self.sprite_group.add(new_piece)
            self.pieces.append(new_piece)

    def move_piece(self, uid, end):
        piece = self.get_piece_by_uid(uid)
        piece.set_new_loc(end)

    def get_piece_by_uid(self, uid):
        """Retrieves pieces sprite object from the list by uid.
        :return Piece: A piece sprite object.
        """
        for piece in self.pieces:
            if piece.uid == uid:
                return piece

    def get_piece(self, loc):
        view_loc = Conf.loc_to_view(loc[0], loc[1])
        for piece in self.pieces:
            if piece.is_collided(view_loc):
                return piece

    def set_piece_selected(self, uid, val):
        """Retrieves piece and sets it's value to selected/deselected.
        :param uid: Piece uid.
        :param val: value 1 is selected 0 is deselected.
        """
        piece = self.get_piece_by_uid(uid)
        if piece:
            piece.selected = val

    def set_available_locs(self, locs, val):
        for loc in locs:
            view_loc = Conf.loc_to_view(loc[0], loc[1])
            for field in self.fields:
                if field.is_collided(view_loc):
                    field.highlighted = val


class OptionsView(MVCView):
    def __init__(self, ev_manager):
        MVCView.__init__(self, ev_manager)
        self.fields = []
        self.pieces = []
        # Load images
        # Load sound


class Piece(DirtySprite):
    def __init__(self, a_piece, loc):
        DirtySprite.__init__(self)
        self.image = pygame.Surface([Conf.PIECE_SIZE, Conf.PIECE_SIZE])
        self.image.fill(Conf.COLOURS[a_piece.value])
        self.rect = self.image.get_rect()
        self.rect.center = loc
        self.new_loc = loc
        self.player = a_piece.value
        self.uid = a_piece.uid
        self.selected = 0
        self.dirty = 2
        # self.dragged = False

    def is_collided(self, view_loc):
        return self.rect.collidepoint(view_loc)

    def set_new_loc(self, loc):
        self.new_loc = Conf.loc_to_view(loc[0], loc[1])

    def update(self):
        if self.selected:
            self.image.fill(Conf.COL_BLUE)
        else:
            self.image.fill(Conf.COLOURS[self.player])
        if not self.rect.center == self.new_loc:
            x, y = self.rect.center
            new_x, new_y = self.new_loc
            dx = new_x - x
            dy = new_y - y

            if dx > 0:
                if dx > Conf.PIECE_FAST:
                    dx = Conf.PIECE_FAST
            elif dx < 0:
                if dx < -Conf.PIECE_FAST:
                    dx = -Conf.PIECE_FAST

            if dy > 0:
                if dy > Conf.PIECE_FAST:
                    dy = Conf.PIECE_FAST
            elif dy < 0:
                if dy < -Conf.PIECE_FAST:
                    dy = -Conf.PIECE_FAST
            self.rect.center = (x + dx, y + dy)


class Field(DirtySprite):
    def __init__(self, field_type, loc):
        DirtySprite.__init__(self)
        self.image = pygame.Surface([Conf.PIECE_SIZE, Conf.PIECE_SIZE])
        self.image.fill(Conf.COLOURS[field_type])
        self.rect = self.image.get_rect()
        self.rect.center = loc
        self.highlighted = 0
        self.dirty = 2

    def is_collided(self, view_loc):
        return self.rect.collidepoint(view_loc)

    def update(self):
        if self.highlighted:
            self.image.fill(Conf.COL_BLUE)
        else:
            self.image.fill(Conf.COL_WHITE)


class Button(DirtySprite):
    def __init__(self, loc, imgs):
        DirtySprite.__init__(self)
        self.imgs = imgs
        self.image = self.imgs[0]
        self.rect = self.image.get_rect()
        self.rect.center = loc
        self.selected = 0
        self.dirty = 2

    def set_selected(self, val):
        self.selected = val

    def update(self):
        if self.selected:
            self.image = self.imgs[1]
        else:
            self.image = self.imgs[0]


class BackGround(DirtySprite):
    def __init__(self):
        DirtySprite.__init__(self)
        self.image = Utils.load_image('bg_plain')
        self.rect = self.image.get_rect()
        self.rect.topleft = 0, 0
        self.dirty = 2


if __name__ == "__main__":
    raise Exception("Unexpected")
