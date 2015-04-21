import sys
import traceback
import time
import copy
import math
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
        if Conf.OPT_OPTIONS.get(Conf.AI_DIF) == Conf.OPT_EASY:
            self.random_move()
        elif Conf.OPT_OPTIONS.get(Conf.AI_DIF) == Conf.OPT_MEDIUM:
            self.better_move()

    def find_pieces_and_moves(self):
        self.pieces = {}
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

    def better_move(self):
        datas = []
        cpus = []
        try:
            if len(self.pieces) > 0:
                for key, value in self.pieces.iteritems():
                    if len(value) > 0:
                        for loc in value:
                            cpu = CrazyCPU(key, loc, copy.deepcopy(self.board), datas, self.player)
                            cpus.append(cpu)
                            cpu.start()

                waiting = 1
                while waiting:
                    x = 0
                    for cpu in cpus:
                        if cpu.is_alive():
                            x = 1
                    waiting = x

                smallest = 1001.0
                for a_val in datas:
                    if a_val.val < smallest:
                        smallest = a_val.val
                        start, end = a_val.loc_s, a_val.loc_e

                data = {'skip': 0, 'start': start, 'end': end}
                print datas
            else:
                # In case there are no moves
                data = {'skip': 1}
            self.post(AIMovedEvent(data), Conf.MODEL)
        except:
            e = sys.exc_info()[0]
            print '>>>>>>>>>>> Fatal Error in: CRAXZY CPUSSSSSSSSSS'
            print e
            traceback.print_exc()
            # fight back
            data = {'skip': 1}
            self.post(AIMovedEvent(data), Conf.MODEL)


class Data(object):
    def __init__(self, val, loc_s, loc_e):
        self.val = val
        self.loc_s = loc_s
        self.loc_e = loc_e

    def __str__(self):
        return str(self.val) + " " + str(self.loc_s) + " " + str(self.loc_e)

    def __repr__(self):
        return self.__str__()

class CrazyCPU(AI):
    cnt = 0

    def __init__(self, loc_s, loc_e, board_copy, data_list, player):
        AI.__init__(self, EventManager())
        self.board = board_copy
        self.data_list = data_list
        self.loc_s = loc_s
        self.loc_e = loc_e
        CrazyCPU.cnt += 1
        self.cnt = CrazyCPU.cnt
        if Conf.DEBUG:
            print '[CRAZY CPU #' + str(self.cnt) + ' STARTED]'
        self.free_home = []
        self.free_home2 = []
        self.player = player
        self.shortest = 100

    def run(self):
        self.make_free_home()
        self.make_move(self.loc_s, self.loc_e)
        self.make_free_home2()
        # if len(self.free_home2) < len(self.free_home):
        #     self.data_list.append(Data(0, self.loc_s, self.loc_e))
        # else:
        self.find_pieces_and_moves()
        self.data_list.append(Data(self.find_shortest(), self.loc_s, self.loc_e))
        if Conf.DEBUG:
            print '[CRAZY CPU #' + str(self.cnt) + ' FINISHED]'

    def make_free_home(self):
        for loc in self.board.win_sectors.get(self.player):
            self.free_home.append(loc)

    def make_free_home2(self):
        for loc in self.board.win_sectors.get(self.player):
            self.free_home2.append(loc)

    def make_move(self, start_loc, end_loc):
        """Change actual model values for pieces stored.
        :param start_loc: location(model based).
        :param end_loc: location(model based).
        Method swaps pieces at given locations.
        """
        temp = self.board.get_field(start_loc)
        self.board.set_field(start_loc, self.board.get_field(end_loc))
        self.board.set_field(end_loc, temp)

    def find_shortest(self):
        valr = 200
        print self.free_home2
        print self.pieces
        if len(self.pieces) > 0:
            for key, value in self.pieces.iteritems():
                if key not in self.board.win_sectors[self.player]:
                    for home_loc in self.free_home2:
                        dx = abs(key[0]-home_loc[0])
                        dy = abs(key[1]-home_loc[1])
                        val = math.sqrt(dx*dx+dy*dy)
                        print val
                        print self.loc_s
                        print self.loc_e
                        if 1.41 < val < 1.42:
                            val = 12
                            valr = val

                        valr += val
        return valr