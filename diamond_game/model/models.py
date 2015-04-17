from diamond_game import *


class MasterModel(MVCObject):
    def __init__(self, ev_manager):
        MVCObject.__init__(self, ev_manager)
        self.model_classes = {'menu': [MenuModel], 'game': [GameModel], 'options': [OptionsModel]}
        self.sub_models = []
        self.switch_model('menu')

    def notify(self, event):
        # Handle events
        if isinstance(event, SwitchScreenEvent):
            self.switch_model(event.value)
        else:
            for model in self.sub_models:
                # Look for a model that accepts event
                if model.does_handle_event(event):
                    # Let model handle event
                    model.handle_event(event)
                    # Stop other models from handling current event
                    break

    def switch_model(self, key):
        if not self.model_classes.has_key(key):
            raise NotImplementedError
        self.sub_models = []
        for model_class in self.model_classes[key]:
            new_model = model_class(self.event_manager)
            self.sub_models.append(new_model)


class MenuModel(MVCObject):
    def __init__(self, ev_manager):
        MVCObject.__init__(self, ev_manager)
        self.data = ['game', 'options', 'exit']
        self.chosen = 0

    def does_handle_event(self, event):
        if isinstance(event, TickEvent):
            return 0
        return 1

    def handle_event(self, event):
        if isinstance(event, MenuPrevEvent):
            self.post(MenuUnSelectEvent(self.chosen))
            if self.chosen == 0:
                self.chosen = len(self.data) - 1
            else:
                self.chosen -= 1
            self.post(MenuSelectEvent(self.chosen))
        elif isinstance(event, MenuNextEvent):
            self.post(MenuUnSelectEvent(self.chosen))
            if self.chosen < len(self.data)-1:
                self.chosen += 1
            else:
                self.chosen = 0
            self.post(MenuSelectEvent(self.chosen))
        elif isinstance(event, ButtonHoverEvent):
            self.post(MenuUnSelectEvent(self.chosen))
            self.chosen = event.value
            self.post(MenuSelectEvent(self.chosen))
        elif isinstance(event, MenuPressEvent):
            if self.data[self.chosen] == 'exit':
                self.post(QuitEvent())
            else:
                self.post(SwitchScreenEvent(self.data[self.chosen]))


class GameModel(MVCObject):
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

    def handle_event(self, event):
        if isinstance(event, MenuPrevEvent):
            self.post(MenuUnSelectEvent(self.chosen))
            if self.chosen == 0:
                self.chosen = len(self.data) - 1
            else:
                self.chosen -= 1
            self.post(MenuSelectEvent(self.chosen))
        elif isinstance(event, MenuNextEvent):
            self.post(MenuUnSelectEvent(self.chosen))
            if self.chosen < len(self.data)-1:
                self.chosen += 1
            else:
                self.chosen = 0
            self.post(MenuSelectEvent(self.chosen))
        elif isinstance(event, ButtonHoverEvent):
            self.post(MenuUnSelectEvent(self.chosen))
            self.chosen = event.value
            self.post(MenuSelectEvent(self.chosen))
        elif isinstance(event, MenuPressEvent):
            if self.data[self.chosen] == 'exit':
                self.post(QuitEvent())
            else:
                self.post(SwitchScreenEvent(self.data[self.chosen]))


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

    def handle_event(self, event):
        if isinstance(event, MenuPrevEvent):
            self.post(MenuUnSelectEvent(self.chosen))
            if self.chosen == 0:
                self.chosen = len(self.data) - 1
            else:
                self.chosen -= 1
            self.post(MenuSelectEvent(self.chosen))
        elif isinstance(event, MenuNextEvent):
            self.post(MenuUnSelectEvent(self.chosen))
            if self.chosen < len(self.data)-1:
                self.chosen += 1
            else:
                self.chosen = 0
            self.post(MenuSelectEvent(self.chosen))
        elif isinstance(event, ButtonHoverEvent):
            self.post(MenuUnSelectEvent(self.chosen))
            self.chosen = event.value
            self.post(MenuSelectEvent(self.chosen))
        elif isinstance(event, MenuPressEvent):
            if self.data[self.chosen] == 'exit':
                self.post(QuitEvent())
            else:
                self.post(SwitchScreenEvent(self.data[self.chosen]))

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
