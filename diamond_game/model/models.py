from diamond_game import *


class MasterModel(MVCObject):
    def __init__(self, ev_manager):
        MVCObject.__init__(self, ev_manager, '[model]')
        self.id = Conf.MODEL
        self.sub_classes = {Conf.MENU: [MenuModel],
                            Conf.GAME: [GameModel],
                            Conf.OPTIONS: [OptionsModel]}
        self.switch_sub_modules(Conf.MENU)

    @property
    def get_next_event(self):
        return self.event_manager.get_next_model_event()

    def run(self):
        running = 1
        while running:
            # Check model's event queue
            event = self.get_next_event
            # Handle events
            # If quit event then terminate
            if isinstance(event, QuitEvent):
                print self.thread_name + ' is shutting down'
                running = 0
            elif isinstance(event, SwitchScreenEvent):
                # Switch sub_modules on request
                self.switch_sub_modules(event.value)
            else:
                for a_model in self.sub_modules:
                    # Look for a model that accepts event
                    if a_model.does_handle_event(event):
                        # Let model handle event
                        a_model.handle_event(event)
                        # Stop other models from handling current event
                        break


class MenuModel(MVCObject):
    def __init__(self, ev_manager):
        MVCObject.__init__(self, ev_manager, '[MenuModel]')
        self.data = [Conf.GAME, Conf.OPTIONS, Conf.EXIT]
        self.chosen = 0

    def does_handle_event(self, event):
        if isinstance(event, TickEvent):
            return 0
        return 1

    def handle_event(self, event):
        if isinstance(event, MenuPrevEvent):
            self.post(MenuUnSelectEvent(self.chosen), Conf.VIEW)
            if self.chosen == 0:
                self.chosen = len(self.data) - 1
            else:
                self.chosen -= 1
            self.post(MenuSelectEvent(self.chosen), Conf.VIEW)
        elif isinstance(event, MenuNextEvent):
            self.post(MenuUnSelectEvent(self.chosen), Conf.VIEW)
            if self.chosen < len(self.data)-1:
                self.chosen += 1
            else:
                self.chosen = 0
            self.post(MenuSelectEvent(self.chosen), Conf.VIEW)
        elif isinstance(event, ButtonHoverEvent):
            self.post(MenuUnSelectEvent(self.chosen), Conf.VIEW)
            self.chosen = event.value
            self.post(MenuSelectEvent(self.chosen), Conf.VIEW)
        elif isinstance(event, MenuPressEvent):
            if self.data[self.chosen] == Conf.EXIT:
                self.post(QuitEvent(), Conf.ALL)
            else:
                self.post(SwitchScreenEvent(self.data[self.chosen]), Conf.ALL)


class GameModel(MVCObject):
    def __init__(self, ev_manager):
        MVCObject.__init__(self, ev_manager, '[GameModel]')
        self.current_player = Conf.empty
        size_player_triangle_base = Conf.default_size_player_base
        self.board = Board(size_player_triangle_base)
        self.number_of_players = 2
        self.ai_players = []
        self.set_ai_at_random()
        self.board.init_board(Conf.num_players)
        self.current_player = Conf.p1
        self.piece_selected = 0
        self.piece_selected_loc = (-1, -1)
    # initialise game for players set with the board
    # ai players is the list of player positions that
    # indicates that a player at that position is managed by ai
    #
    # current player is set from 1..6 as defined in config

    def does_handle_event(self, event):
        if isinstance(event, TickEvent):
            return 0
        return 1

    def handle_event(self, event):
        # Whenever View is ready provide pieces and board
        if isinstance(event, SubModulesLoadedEvent):
            if event.module == Conf.VIEW and event.sub_module == Conf.GAME:
                self.post(BoardCreatedEvent(self.get_board_grid()), Conf.VIEW)
                self.post(PiecesCreatedEvent(self.get_pieces()), Conf.VIEW)
        elif isinstance(event, GameObjectClickEvent):
            if event.typ == Conf.GAME_CONTROL:
                pass
                # music on/off
                # sound on/off
                # save/load
                # restart
            elif event.typ == Conf.GAME_PLAY:
                # Piece not selected
                if self.piece_selected == 0:
                    if not self.is_own_piece(event.value):
                        return
                    else:
                        self.select_piece(event.value)
                elif self.piece_selected == 1:
                    # Piece already selected
                    if self.piece_selected_loc == event.value:
                        # Piece deselection
                        self.deselect_piece(event.value)
                    elif self.is_own_piece(event.value):
                        # Piece reselection
                        self.reselect_piece(self.piece_selected_loc, event.value)
                    elif self.is_valid_move(self.piece_selected_loc, event.value):
                        # Piece movement
                        self.move(event.value)
                        self.deselect_piece(event.value)

                # select/deselect -> show/remove hints
                # move
                # undo move

    def select_piece(self, loc):
        self.piece_selected = 1
        self.piece_selected_loc = loc
        self.post(PieceSelectedEvent(loc), Conf.VIEW)

    def deselect_piece(self, loc):
        self.piece_selected = 0
        self.piece_selected_loc = (-1, -1)
        self.post(PieceDeSelectedEvent(loc), Conf.VIEW)

    def reselect_piece(self, loc_no, loc_yes):
        self.post(PieceDeSelectedEvent(loc_no), Conf.VIEW)
        self.post(PieceSelectedEvent(loc_yes), Conf.VIEW)
        self.piece_selected_loc = loc_yes

    def is_valid_move(self, loc_start, loc_end):
        # self.is_reachable(loc_start, loc_end)
        # create list of rechable fields, from loc_start
        # if loc_end in the list
        # and is empty of course
        return 1

    def is_reachable(self, loc_start, loc_end):
        return 1

    def set_ai_at_random(self):
        pass
        # ai_players = [0, 1]

    def not_move_own(self, loc):
        return self.board.get_field(loc) != self.current_player

    def not_free_field(self, loc):
        return self.board.get_field(loc) != 0

    def is_own_piece(self, loc):
        piece = self.board.get_field(loc)
        return piece == self.current_player

    def is_reachable_field(self, loc):
        return 1

    def not_reachable_field(self, loc):
        return 0

    def valid_move(self):
        if self.not_move_own():
            return False
        if self.not_free_field():
            return False
        if self.not_reachable_field():
            return False

    def make_move(self, start, end):
        self.board.set_field(end, self.board.get_field(start))
        self.board.set_field(start, 0)

    def move(self, loc):
        self.make_move(self.piece_selected_loc, loc)
        self.post(PieceMoveEvent(self.piece_selected_loc, loc), Conf.VIEW)
        self.piece_selected = 0
        self.piece_selected_loc = (-1, -1)
        self.next_player()

    def next_player(self):
        if self.current_player < self.number_of_players:
            self.current_player += 1
        else:
            self.current_player = 1

    def is_ai_player(self, player):
        if self.ai_players.__contains__(player):
            return True
        return False

    # returns dimension of board grid as a tuple
    def get_grid_dimensions(self):
        return self.board.SIZE_BOARD_X_GRID, self.board.SIZE_BOARD_Y_GRID

    def get_pieces(self):
        pieces = []
        for y in range(self.board.SIZE_BOARD_Y_GRID):
            for x in range(self.board.SIZE_BOARD_X_GRID):
                field = self.board.get_field((x, y))
                if field != Conf.non_playable and field != Conf.empty:
                    pieces.append({'x': x, 'y': y, 'val': field})
        return pieces

    def get_board_grid(self):
        fields = []
        for y in range(self.board.SIZE_BOARD_Y_GRID):
            for x in range(self.board.SIZE_BOARD_X_GRID):
                field = self.board.get_field((x, y))
                if field != Conf.non_playable:
                    fields.append({'x': x, 'y': y, 'val': 0})
        return fields


class OptionsModel(MVCObject):
    def __init__(self, ev_manager):
        MVCObject.__init__(self, ev_manager)
        self.current_player = Conf.empty
        size_player_triangle_base = Conf.default_size_player_base
        self.board = Board(size_player_triangle_base)
        self.ai_players = []
        self.set_ai_at_random()
        self.board.init_board(Conf.num_players)
        self.current_player = Conf.p1
        self.post(BoardCreatedEvent(self.get_board_grid()))
        self.post(PiecesCreatedEvent(self.get_pieces()))
    # initialise game for players set with the board
    # ai players is the list of player positions that
    # indicates that a player at that position is managed by ai
    #
    # current player is set from 1..6 as defined in config

    def set_ai_at_random(self):
        pass
        # ai_players = [0, 1]

    def not_move_own(self, loc):
        return self.board.get_field(loc) != self.current_player

    def not_free_field(self, loc):
        return self.board.get_field(loc) != 0

    def not_reachable_field(self):
        return False

    def valid_move(self):
        if self.not_move_own():
            return False
        if self.not_free_field():
            return False
        if self.not_reachable_field():
            return False

    def make_move(self, start, end):
        self.board.set_field(end, self.board.get_field(start))
        self.board.set_field(start, 0)

    def move(self, start, end):
        if self.valid_move():
            self.make_move(start, end)

    def next_player(self):
        if self.current_player < self.number_of_players:
            self.current_player += 1
        else:
            self.current_player = 1

    def is_ai_player(self, player):
        if self.ai_players.__contains__(player):
            return True
        return False

    # returns dimension of board grid as a tuple
    def get_grid_dimensions(self):
        return self.board.SIZE_BOARD_X_GRID, self.board.SIZE_BOARD_Y_GRID

    def get_pieces(self):
        pieces = []
        for y in range(self.board.SIZE_BOARD_Y_GRID):
            for x in range(self.board.SIZE_BOARD_X_GRID):
                field = self.board.get_field((x, y))
                if field != Conf.non_playable and field != Conf.empty:
                    pieces.append({'x': x, 'y': y, 'val': field})
        return pieces

    def get_board_grid(self):
        fields = []
        for y in range(self.board.SIZE_BOARD_Y_GRID):
            for x in range(self.board.SIZE_BOARD_X_GRID):
                field = self.board.get_field((x, y))
                if field != Conf.non_playable:
                    fields.append({'x': x, 'y': y, 'val': 0})
        return fields

    def does_handle_event(self, event):
        if isinstance(event, TickEvent):
            return 0
        return 1

    # def handle_event(self, event):
    #     if isinstance(event, MenuPrevEvent):
    #         self.post(MenuUnSelectEvent(self.chosen))
    #         if self.chosen == 0:
    #             self.chosen = len(self.data) - 1
    #         else:
    #             self.chosen -= 1
    #         self.post(MenuSelectEvent(self.chosen))
    #     elif isinstance(event, MenuNextEvent):
    #         self.post(MenuUnSelectEvent(self.chosen))
    #         if self.chosen < len(self.data)-1:
    #             self.chosen += 1
    #         else:
    #             self.chosen = 0
    #         self.post(MenuSelectEvent(self.chosen))
    #     elif isinstance(event, ButtonHoverEvent):
    #         self.post(MenuUnSelectEvent(self.chosen))
    #         self.chosen = event.value
    #         self.post(MenuSelectEvent(self.chosen))
    #     elif isinstance(event, MenuPressEvent):
    #         if self.data[self.chosen] == 'exit':
    #             self.post(QuitEvent())
    #         else:
    #             self.post(SwitchScreenEvent(self.data[self.chosen]))

'''
Board class. Board can be customized to:
    - How many players will play (2-6)
    - What is the size of player triangle: hence how many pieces he has

To resize board new instance should be created with desired size

To change number of players reinitiate the board with desired player size
'''


class Board(object):
    # creates empty board
    def __init__(self, size_player_base=4):
        self.SIZE_PLAYER_BASE = size_player_base
        self.SIZE_PLAYER_BASE_GRID = (self.SIZE_PLAYER_BASE * 2) - 1
        self.SIZE_BOARD_CENTER = self.SIZE_PLAYER_BASE + 1
        self.SIZE_TRIANGLE_BASE = (self.SIZE_PLAYER_BASE * 3) + 1
        self.SIZE_BOARD_X_GRID = (self.SIZE_TRIANGLE_BASE * 2) - 1
        self.SIZE_BOARD_Y_GRID = (self.SIZE_PLAYER_BASE * 4) + 1
        self.board = []
        self.make_board()

    def get_field(self, loc):
        x = loc[0]
        y = loc[1]
        return self.board[y][x]

    def set_field(self, loc, val):
        x = loc[0]
        y = loc[1]
        self.board[y][x] = val

    # creates a row for the board where num_fields is number of playable fields in that row
    def mrow(self, num_fields):
        empties = num_fields-1  # empty spaces between playable for triangle structure
        cnt_non_playable = (self.SIZE_BOARD_X_GRID - num_fields - empties)/2
        margin = [Conf.non_playable] * cnt_non_playable
        center = []
        for i in range(1, num_fields + empties + 1):
            if i % 2 == 0:
                center.append(Conf.non_playable)
            else:
                center.append(Conf.empty)
        return margin + center + margin

    # creates a board based on player base size
    def make_board(self):
        del self.board[:]  # destroy previous board
        cnt = 0
        last_ind = 0
        for i in range(1, self.SIZE_BOARD_Y_GRID+1):
            if i/self.SIZE_BOARD_CENTER == 0:  # make rows in player 1 zone
                self.board.append(self.mrow(i))
            elif i/self.SIZE_BOARD_CENTER == 1:  # make rows between 1st player zone to the center
                self.board.append(self.mrow(self.SIZE_TRIANGLE_BASE-cnt))
                cnt += 1
                last_ind = len(self.board) - 1
            else:  # else reflect structure made for the top half
                last_ind -= 1
                self.board.append(list(self.board[last_ind]))

    # initiates created board with player pieces
    def init_board(self, num_players=2):
        self.make_board()
        players = [Conf.p1, Conf.p3, Conf.p6, Conf.p5, Conf.p4, Conf.p2]
        for index in range(len(players)):
            if players[index] > num_players:
                players[index] = Conf.empty
        i = self.SIZE_PLAYER_BASE_GRID
        for y in range(self.SIZE_BOARD_Y_GRID):
            row = self.board[y]
            if y/self.SIZE_PLAYER_BASE == 0:
                for x in range(self.SIZE_BOARD_X_GRID):
                    if row[x] == 0:
                        row[x] = players[0]
            elif y/self.SIZE_PLAYER_BASE == 1:
                for x in range(self.SIZE_BOARD_X_GRID):
                    if row[x] == 0:
                        if x < i:
                            row[x] = players[1]
                        elif x + i >= self.SIZE_BOARD_X_GRID:
                            row[x] = players[2]
                i -= 1
            elif (y-1)/self.SIZE_PLAYER_BASE == 2:
                i += 1
                for x in range(self.SIZE_BOARD_X_GRID):
                    if row[x] == 0:
                        if x < i:
                            row[x] = players[3]
                        elif x + i >= self.SIZE_BOARD_X_GRID:
                            row[x] = players[4]

            elif (y-1)/self.SIZE_PLAYER_BASE == 3:
                for x in range(self.SIZE_BOARD_X_GRID):
                    if row[x] == 0:
                        row[x] = players[5]

    # for debug purposes
    def print_board(self):
        line = ''
        for y in range(self.SIZE_BOARD_Y_GRID):
            for x in range(self.SIZE_BOARD_X_GRID):
                if self.board[y][x] == -1:
                    line += '_'
                elif self.board[y][x] == 0:
                    line += 'x'
                else:
                    line += str(self.board[y][x])
            print line
            line = ''


if __name__ == "__main__":
    raise Exception("Unexpected")
