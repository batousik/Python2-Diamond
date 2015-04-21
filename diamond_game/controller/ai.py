import sys
import traceback
import time
from diamond_game import *
from diamond_game.model.models import Board
import random


class AI(MVCObject):
    def __init__(self, ev_manager):
        MVCObject.__init__(self, ev_manager, '[ai]')
        self.id = Conf.AI
        self.board = Board()
        self.pieces = {}
        self.player = 0
        self.available_locations = []
        self.piece_selected_loc = (-1, -1)
        self.counter = 0

    @property
    def get_next_event(self):
        return self.event_manager.get_next_ai_event()

    # noinspection PyBroadException
    def run(self):
        running = 1
        try:
            while running:
                # Check if ai is required
                event = self.get_next_event
                # Handle events
                # If quit event then terminate
                if isinstance(event, QuitEvent):
                    print self.thread_name + ' is shutting down'
                    running = 0
                elif isinstance(event, AIMakeMoveEvent):
                    # time.sleep(1)
                    self.counter += 1
                    self.make_move(event.data)
        except:
            e = sys.exc_info()[0]
            print '>>>>>>>>>>> Fatal Error in: ' + self.thread_name
            print e
            traceback.print_exc()
            self.post(QuitEvent(), Conf.ALL)

    def make_move(self, data):
        self.board = data['board']
        self.player = data['player']
        self.pieces = {}
        self.find_pieces_and_moves()
        self.random_move()

    def find_pieces_and_moves(self):
        for x in range(self.board.SIZE_BOARD_X_GRID):
            for y in range(self.board.SIZE_BOARD_Y_GRID):
                if self.board.get_field((x, y)).value == self.player:
                    self.get_available_moves(x, y)
                    if len(self.available_locations):
                        self.pieces[(x, y)] = self.available_locations

    def get_available_moves(self, x, y):
        self.available_locations = []
        self.piece_selected_loc = (x, y)
        self.add_normal_moves(self.piece_selected_loc)
        self.add_jump_moves(self.piece_selected_loc)

    def add_normal_moves(self, loc):
        """Add normal moves to the list of available moves.
        :param loc: location(model based) points from where move is started.
        Method checks piece surroundings and if it is possible to move there
        adds it to available locations
        """
        for direction in Conf.NORMAL_DIRECTIONS:
            new_loc = (loc[0] + direction[0], loc[1] + direction[1])
            if 0 <= new_loc[0] < self.board.SIZE_BOARD_X_GRID and \
                                    0<= new_loc[1] < self.board.SIZE_BOARD_Y_GRID:
                if self.board.get_field(new_loc).value == Conf.EMPTY:
                    self.available_locations.append(new_loc)

    def add_jump_moves(self, loc):
        """Add jump moves to the list of available moves.
        :param loc: location(model based) points from where move is started.
        Method checks where a piece could jump and if it can then move is added
        to available locations and jump moves is called recursively.
        Have to be careful not to add and recurse on duplicate locations.
        """
        # go through adjacent field
        for i in range(len(Conf.NORMAL_DIRECTIONS)):
            jump_over_loc = (loc[0] + Conf.NORMAL_DIRECTIONS[i][0], loc[1] + Conf.NORMAL_DIRECTIONS[i][1])
            # if field is in bounds of data structure
            if 0 <= jump_over_loc[0] < self.board.SIZE_BOARD_X_GRID and \
                                    0<= jump_over_loc[1] < self.board.SIZE_BOARD_Y_GRID:
                # if field is a piece
                if not self.board.get_field(jump_over_loc).value == Conf.EMPTY and \
                        not self.board.get_field(jump_over_loc).value == Conf.NON_PLAYABLE:
                    # get jump to location
                    new_loc = (loc[0] + Conf.JUMP_DIRECTIONS[i][0], loc[1] + Conf.JUMP_DIRECTIONS[i][1])
                    # if jump to location is in bounds
                    if 0 <= new_loc[0] < self.board.SIZE_BOARD_X_GRID and \
                                            0<= new_loc[1] < self.board.SIZE_BOARD_Y_GRID:
                        # if jump to location is free
                        if self.board.get_field(new_loc).value == Conf.EMPTY:
                            # if this location doesnt already exist and not the starting location
                            if new_loc not in self.available_locations and \
                                    not new_loc == self.piece_selected_loc:
                                self.available_locations.append(new_loc)
                                self.add_jump_moves(new_loc)

    def random_move(self):
        random.seed()
        if len(self.pieces) > 0:
            start = random.choice(self.pieces.keys())

            end = random.choice(self.pieces.get(start))
            data = {'skip': 0, 'start': start, 'end': end}
        else:
            # In case there are no moves
            data = {'skip': 1}
        self.post(AIMovedEvent(data), Conf.MODEL)

