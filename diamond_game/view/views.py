import math
import traceback
from __builtin__ import isinstance
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
                            Conf.OPTIONS: [OptionsView],
                            Conf.DIAMOND: [DiamondOptionsView],
                            Conf.CHINESE_CHECKERS: [ChineseCheckersOptionsView],
                            Conf.END_GAME: [DiamondOptionsView]}

        # perform some set up
        # window caption
        pygame.display.set_caption("Chinese Checkers v 0.7")
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
            traceback.print_exc()
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
        self.board_sprite = BoardSprite()
        self.sprite_group.add(self.board_sprite)
        # list of pieces sprites
        self.pieces = []
        self.fields = []
        self.click_sprites = LayeredDirty()
        self.board_rad = 380
        self.pieces_width = 2 * self.board_rad * math.cos(math.pi/3)
        self.amount_x = 10
        self.x_separation = 10
        self.y_separation = 10
        self.piece_rad = 10
        self.piece_size = 10
        self.board_x_offset = 10
        self.board_y_offset = 10
        self.center = (10, 10)
        # Load images

    def does_handle_event(self, event):
        return 1

    def handle_event(self, event):
        if isinstance(event, BoardCreatedEvent):
            self.fields_start_locs = event.value
            self.do_view_calc(event.dimention)
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
                    self.post(
                        GameObjectClickEvent(Conf.GAME_PLAY, self.loc_to_model(sprite.rect.center)),
                        Conf.MODEL)
                    break

    def create_board(self):
        """
        Create Field sprites, with colour (empty)
        from list of received locations
        """
        for field in self.fields_start_locs:
            loc = self.loc_to_view(field[0], field[1])
            new_field = Field(loc, self.piece_size)
            self.sprite_group.add(new_field)
            self.click_sprites.add(new_field)
            self.fields.append(new_field)

    def create_pieces(self):
        self.pieces = []
        for piece in self.pieces_start_locs:
            loc = self.loc_to_view(piece['x'], piece['y'])
            new_piece = Piece(piece['piece'], loc, self.piece_size)
            self.click_sprites.add(new_piece)
            self.sprite_group.add(new_piece)
            self.pieces.append(new_piece)

    def move_piece(self, uid, end):
        piece = self.get_piece_by_uid(uid)
        piece.set_new_loc(self.loc_to_view(end[0], end[1]))

    def get_piece_by_uid(self, uid):
        """Retrieves pieces sprite object from the list by uid.
        :return Piece: A piece sprite object.
        """
        for piece in self.pieces:
            if piece.uid == uid:
                return piece

    def get_piece(self, loc):
        view_loc = self.loc_to_view(loc[0], loc[1])
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
            view_loc = self.loc_to_view(loc[0], loc[1])
            for field in self.fields:
                if field.is_collided(view_loc):
                    field.highlighted = val

    def do_view_calc(self, dimention):
        self.center = (dimention[0]/2, dimention[1]/2)
        self.amount_x = dimention[0]
        self.x_separation = int(self.pieces_width/self.amount_x)
        self.y_separation = int(math.sin(math.pi/3) * self.x_separation)
        self.piece_rad = self.x_separation / 2
        self.piece_size = self.x_separation
        # self.board_x_offset = self.piece_rad + Conf.BOARD_CENTER[0] - self.pieces_width/2
        # self.board_y_offset = self.piece_rad + 40

    def loc_to_view(self, x, y):
        new_x = Conf.BOARD_REAL_CENTER[0] + (x-self.center[0]) * self.piece_size
        new_y = Conf.BOARD_REAL_CENTER[1] + (y-self.center[1]) * (self.piece_size + self.y_separation)
        return new_x, new_y

    def loc_to_model(self, loc):
        new_x = (loc[0] - Conf.BOARD_REAL_CENTER[0]) / self.piece_size + self.center[0]
        new_y = (loc[1] - Conf.BOARD_REAL_CENTER[1]) / (self.piece_size + self.y_separation) + self.center[1]
        return int(new_x), int(new_y)


class OptionsView(MVCView):
    def __init__(self, ev_manager):
        MVCView.__init__(self, ev_manager, '[view_options1]')
        b1 = Button2(Conf.B_OPT_1_0, 'b_opt_1_0', Conf.DIAMOND)
        b2 = Button2(Conf.B_OPT_1_1, 'b_opt_1_1', Conf.CHINESE_CHECKERS)
        self.click_sprites = LayeredDirty()
        self.click_sprites.add(b1)
        self.click_sprites.add(b2)
        self.sprite_group.add(b1)
        self.sprite_group.add(b2)

    def does_handle_event(self, event):
        return 1

    def handle_event(self, event):
        if isinstance(event, MouseClickEvent):
            for sprite in self.click_sprites:
                if sprite.rect.collidepoint(event.position):
                    Conf.GAME_CHOSEN = sprite.an_id
                    self.post(OptionsClickEvent(sprite.an_id), Conf.MODEL)
                    break


class DiamondOptionsView(MVCView):
    def __init__(self, ev_manager):
        MVCView.__init__(self, ev_manager, '[view_options1]')
        label1 = Label2((200 + 100 + 40, 200 + 100 + 10 - 100 + 15 + 11 + 3))
        self.sprite_group.add(label1)
        self.click_sprites = LayeredDirty()
        imgs = [Utils.load_image('none'), Utils.load_image('human'), Utils.load_image('ai')]
        b_ai = Button3((430 + 100 + 40, 75 + 100), [Utils.load_image('easy'),
                       Utils.load_image('medium')],
                       Conf.AI_DIF, Conf.OPT_OPTIONS.get(Conf.AI_DIF))
        bp1 = Button3((430 + 100 + 40, 75 + 40 + 100), imgs, Conf.BP1, Conf.OPT_OPTIONS.get(Conf.BP1))
        bp2 = Button3((430 + 100 + 40, 75 + 80 + 100), imgs, Conf.BP2, Conf.OPT_OPTIONS.get(Conf.BP2))
        bp3 = Button3((430 + 100 + 40, 75 + 120 + 10 + 100 - 5), imgs, Conf.BP3, Conf.OPT_OPTIONS.get(Conf.BP3))
        self.sprite_group.add(b_ai, bp1, bp2, bp3)
        self.click_sprites.add(b_ai, bp1, bp2, bp3)

    def does_handle_event(self, event):
        return 1

    def handle_event(self, event):
        if isinstance(event, MouseClickEvent):
            for sprite in self.click_sprites:
                if sprite.rect.collidepoint(event.position):
                    self.post(OptionsClickEvent(sprite.an_id), Conf.MODEL)
        elif isinstance(event, OptionButtonStateChangeEvent):
            for sprite in self.click_sprites:
                if sprite.an_id == event.an_id:
                    sprite.state = event.value
                    break


class ChineseCheckersOptionsView(MVCView):
    def __init__(self, ev_manager):
        MVCView.__init__(self, ev_manager, '[view_options1]')
        label1 = Label((200 + 100 + 40, 200 + 100 + 10))
        self.sprite_group.add(label1)
        self.click_sprites = LayeredDirty()
        imgs = [Utils.load_image('none'), Utils.load_image('human'), Utils.load_image('ai')]
        b_ai = Button3((430 + 100 + 40, 75 + 100), [Utils.load_image('easy'),
                       Utils.load_image('medium')],
                       Conf.AI_DIF, Conf.OPT_OPTIONS.get(Conf.AI_DIF))
        bp1 = Button3((430 + 100 + 40, 75 + 40 + 100), imgs, Conf.BP1, Conf.OPT_OPTIONS.get(Conf.BP1))
        bp2 = Button3((430 + 100 + 40, 75 + 80 + 100), imgs, Conf.BP2, Conf.OPT_OPTIONS.get(Conf.BP2))
        bp3 = Button3((430 + 100 + 40, 75 + 120 + 10 + 100 - 5), imgs, Conf.BP3, Conf.OPT_OPTIONS.get(Conf.BP3))
        bp4 = Button3((430 + 100 + 40, 75 + 160 + 10 + 100 - 5), imgs, Conf.BP4, Conf.OPT_OPTIONS.get(Conf.BP4))
        bp5 = Button3((430 + 100 + 40, 75 + 200 + 10 + 100 - 5), imgs, Conf.BP5, Conf.OPT_OPTIONS.get(Conf.BP5))
        bp6 = Button3((430 + 100 + 40, 75 + 240 + 10 + 100 - 5), imgs, Conf.BP6, Conf.OPT_OPTIONS.get(Conf.BP6))
        imgsx22 = [Utils.load_image('1'), Utils.load_image('2'), Utils.load_image('3'),
                 Utils.load_image('4'), Utils.load_image('5'), Utils.load_image('6'),
                 Utils.load_image('7'), Utils.load_image('8'), Utils.load_image('9'),
                 Utils.load_image('10'), Utils.load_image('11'), Utils.load_image('12')]
        bfields = Button3((430 + 100 + 40 + 5, 75 + 240 + 10 + 100 - 5 + 40), imgsx22, Conf.BFIELDS,
                          Conf.OPT_OPTIONS.get(Conf.BFIELDS))
        self.sprite_group.add(b_ai, bp1, bp2, bp3, bp4, bp5, bp6, bfields)
        self.click_sprites.add(b_ai, bp1, bp2, bp3, bp4, bp5, bp6, bfields)

    def does_handle_event(self, event):
        return 1

    def handle_event(self, event):
        if isinstance(event, MouseClickEvent):
            for sprite in self.click_sprites:
                if sprite.rect.collidepoint(event.position):
                    self.post(OptionsClickEvent(sprite.an_id), Conf.MODEL)
        elif isinstance(event, OptionButtonStateChangeEvent):
            for sprite in self.click_sprites:
                if sprite.an_id == event.an_id:
                    sprite.state = event.value
                    break


class EndGameView(MVCView):
    def __init__(self, ev_manager):
        MVCView.__init__(self, ev_manager, '[view_options1]')
        b1 = Button2(Conf.B_OPT_1_0, 'b_opt_1_0', Conf.DIAMOND)
        b2 = Button2(Conf.B_OPT_1_1, 'b_opt_1_1', Conf.CHINESE_CHECKERS)
        self.sprite_group.add(b1)
        self.sprite_group.add(b2)

    def does_handle_event(self, event):
        return 1

    def handle_event(self, event):
        if isinstance(event, MouseClickEvent):
            for sprite in self.sprite_group:
                if sprite.rect.collidepoint(event.position):
                    self.post(OptionsClickEvent(sprite.an_id), Conf.MODEL)
                    break


class Piece(DirtySprite):
    def __init__(self, a_piece, loc, size):
        DirtySprite.__init__(self)
        player = 'p' + str(a_piece.value)
        self.images = [Utils.load_image(player),
                       Utils.load_image(player + '_s')]
        self.images[0] = pygame.transform.scale(self.images[0], (size, size))
        self.images[1] = pygame.transform.scale(self.images[1], (size, size))
        self.image = self.images[0]
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
        self.new_loc = (loc[0], loc[1])

    def update(self):
        if self.selected:
            self.image = self.images[1]
        else:
            self.image = self.images[0]
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
    def __init__(self, loc, size):
        DirtySprite.__init__(self)
        self.images = [Utils.load_image('field'),
                       Utils.load_image('field' + '_h')]
        self.images[0] = pygame.transform.scale(self.images[0], (size, size))
        self.images[1] = pygame.transform.scale(self.images[1], (size, size))
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = loc
        self.highlighted = 0
        self.dirty = 2

    def is_collided(self, view_loc):
        return self.rect.collidepoint(view_loc)

    def update(self):
        if self.highlighted:
            self.image = self.images[0]
        else:
            self.image = self.images[1]


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


class Button2(DirtySprite):
    def __init__(self, loc, img, an_id):
        DirtySprite.__init__(self)
        self.image = Utils.load_image(img)
        self.rect = self.image.get_rect()
        self.rect.center = loc
        self.dirty = 2
        self.an_id = an_id


class Button3(DirtySprite):
    def __init__(self, loc, imgs, an_id, state):
        DirtySprite.__init__(self)
        self.imgs = imgs
        self.state = state
        self.image = imgs[self.state]
        self.rect = self.image.get_rect()
        self.rect.center = loc
        self.dirty = 2
        self.an_id = an_id

    def update(self, *args):
        self.image = self.imgs[self.state]


class Label(DirtySprite):
    def __init__(self, loc):
        DirtySprite.__init__(self)
        self.image = Utils.load_image('label')
        self.rect = self.image.get_rect()
        self.rect.center = loc
        self.dirty = 2


class Label2(DirtySprite):
    def __init__(self, loc):
        DirtySprite.__init__(self)
        self.image = Utils.load_image('label2')
        self.rect = self.image.get_rect()
        self.rect.center = loc
        self.dirty = 2


class BackGround(DirtySprite):
    def __init__(self):
        DirtySprite.__init__(self)
        self.image = Utils.load_image('bg_plain')
        self.rect = self.image.get_rect()
        self.rect.topleft = 0, 0
        self.dirty = 2


class BoardSprite(DirtySprite):
    def __init__(self):
        DirtySprite.__init__(self)
        self.image = Utils.load_image("board")
        self.rect = self.image.get_rect()
        self.rect.topleft = Conf.BOARD_LOC
        self.dirty = 2

if __name__ == "__main__":
    raise Exception("Unexpected")
