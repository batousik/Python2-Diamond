from diamond_game.model.board import Board
from diamond_game.config import Conf


class Model(object):
    def __init__(self):
        self.current_player = Conf.empty
        self.number_of_players = 0
        size_player_triangle_base = Conf.default_size_player_base
        self.board = Board(size_player_triangle_base)
        self.ai_players = []

    def init_game(self, ai_players, players):
        self.number_of_players = len(ai_players) + len(players)
        self.ai_players = ai_players
        self.board.init_board(self.number_of_players)
        self.current_player = 1

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