import sys
import traceback
from diamond_game import *


class MasterModel(MVCObject):
    def __init__(self, ev_manager):
        MVCObject.__init__(self, ev_manager, '[model]')
        self.id = Conf.MODEL
        self.sub_classes = {Conf.MENU: [MenuModel],
                            Conf.GAME: [GameModel],
                            Conf.GAME2: [DiamondGameModel],
                            Conf.OPTIONS: [OptionsModel],
                            Conf.DIAMOND: [DOptionsModel],
                            Conf.CHINESE_CHECKERS: [CCOptionsModel],
                            Conf.END_GAME: [EndGameModel]}
        self.switch_sub_modules(Conf.MENU)

    @property
    def get_next_event(self):
        return self.event_manager.get_next_model_event()

    # noinspection PyBroadException
    def run(self):
        running = 1
        try:
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
        except:
            e = sys.exc_info()[0]
            print '>>>>>>>>>>> Fatal Error in: ' + self.thread_name
            print e
            traceback.print_exc()
            self.post(QuitEvent(), Conf.ALL)


class MenuModel(MVCObject):
    def __init__(self, ev_manager):
        MVCObject.__init__(self, ev_manager, '[MenuModel]')
        self.data = [Conf.GAME, Conf.OPTIONS, Conf.EXIT]
        self.chosen = 0
    # TODO: if selected - do not reselect

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
                if Conf.GAME_CHOSEN == Conf.CHINESE_CHECKERS:
                    self.post(SwitchScreenEvent(self.data[self.chosen]), Conf.ALL)
                elif Conf.GAME_CHOSEN == Conf.DIAMOND:
                    self.post(SwitchScreenEvent(Conf.GAME2), Conf.ALL)


class GameModel(MVCObject):
    def __init__(self, ev_manager):
        MVCObject.__init__(self, ev_manager, '[GameModel]')
        self.ready = 0
        self.current_player = Conf.EMPTY
        self.size_player_triangle_base = Conf.OPT_OPTIONS.get(Conf.BFIELDS) + 1
        self.board = Board(self.size_player_triangle_base)
        self.number_of_players = 0
        self.current_player_index = 0
        self.players = []
        self.ai_players = []
        i = 1
        for key, value in Conf.OPT_OPTIONS.iteritems():
            if not key == Conf.AI_DIF and not key == Conf.BFIELDS:
                if value > Conf.OPT_NONE:
                    self.number_of_players += 1
                    if value == Conf.OPT_AI:
                        self.ai_players.append(i)
                    self.players.append(i)
                i += 1
        self.set_ai_at_random()
        self.current_player = self.players[self.current_player_index]
        self.piece_selected = 0
        self.piece_selected_loc = (-1, -1)
        self.available_locations = []
        self.waiting_for_ai = 0
    # initialise game for players set with the board
    # ai players is the list of player positions that
    # indicates that a player at that position is managed by ai
    #
    # current player is set from 1..6 as defined in config

    def does_handle_event(self, event):
        return 1

    def handle_event(self, event):
        # Whenever View is ready provide pieces and board
        if isinstance(event, SubModulesLoadedEvent):
            # initiate the GAME
            if event.module == Conf.VIEW and event.sub_module == Conf.GAME:
                self.board = Board(self.size_player_triangle_base)
                self.post(BoardCreatedEvent(self.get_board_grid(), self.get_grid_dimensions()), Conf.VIEW)
                self.board.init_board(self.number_of_players)
                self.post(PiecesCreatedEvent(self.get_pieces()), Conf.VIEW)
                self.ready = 1
                # TODO: resize event
                if Conf.DEBUG:
                    print self.get_grid_dimensions()
        elif isinstance(event, GameObjectClickEvent):
            if event.typ == Conf.GAME_CONTROL:
                pass
                # music on/off
                # sound on/off
                # save/load
                # restart
            elif event.typ == Conf.GAME_PLAY:
                if self.is_ai_move():
                    return
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
                        self.reselect_piece(event.value)
                    elif self.is_valid_move(event.value):
                        # Piece movement
                        self.move(event.value)
                        self.deselect_piece(event.value)

                # select/deselect -> show/remove hints
                # move
                # undo move
        elif isinstance(event, TickEvent):
            if self.is_ai_move():
                if not self.waiting_for_ai and self.ready:
                    self.waiting_for_ai = 1
                    self.post(AIMakeMoveEvent(self.collect_data_for_ai()), Conf.AI)
        elif isinstance(event, AIMovedEvent):
            self.process_ai_move(event.data)
            self.waiting_for_ai = 0

    def is_ai_move(self):
        return self.current_player in self.ai_players

    def process_ai_move(self, data):
        if data['skip']:
            self.next_player()
        else:
            self.select_piece(data['start'])
            self.move(data['end'])
            self.deselect_piece(data['end'])

    def collect_data_for_ai(self):
        val = {'board': self.board, 'player': self.current_player}
        return val

    def select_piece(self, loc):
        """Piece select action.
        :param loc: location(model based).
        Method makes unique piece on the board selected
        stores location (m) of the selected piece
        and sets selected flag to true
        PieceSelectedEvent is emmited with piece unique id
        for the view to process.
        Also create a list of available locations and
        emit event with them.
        """
        self.piece_selected = 1
        self.piece_selected_loc = loc
        piece = self.board.get_field(loc)
        self.post(PieceSelectedEvent(piece.uid), Conf.VIEW)
        self.create_available_locs(loc)

    def deselect_piece(self, loc):
        """Piece select action.
        :param loc: location(model based).
        Method deselects selected piece
        sets selected flag to false and location to (-1, -1)
        PieceDeSelectedEvent is emmited with piece unique id
        for the view to process.
        Also remove list of available locations and
        emit event with them removed.
        """
        self.piece_selected = 0
        self.piece_selected_loc = (-1, -1)
        piece = self.board.get_field(loc)
        self.post(PieceDeSelectedEvent(piece.uid), Conf.VIEW)
        self.remove_available_locs()

    def reselect_piece(self, loc_yes):
        """Piece select action.
        :param loc_yes: location(model based) for selected piece.
        :param loc_no: location(model based) for deselected piece.
        Method deselects old piece and selects new piece emmiting
        corresponding PieceSelectedEvent and PieceDeSelectedEvent
        with pieces unique ids for the view to process.
        selected_piece_loc is updated to the new piece.
        Update available locations and emit event
        """
        loc_no = self.piece_selected_loc
        piece_yes = self.board.get_field(loc_yes)
        piece_no = self.board.get_field(loc_no)
        self.post(PieceDeSelectedEvent(piece_no.uid), Conf.VIEW)
        self.post(PieceSelectedEvent(piece_yes.uid), Conf.VIEW)
        self.piece_selected_loc = loc_yes
        self.remove_available_locs()
        self.create_available_locs(loc_yes)

    def create_available_locs(self, loc):
        """Create available locations list.
        :param loc: location(model based) points from where move will be started.
        Method creates list of reachable locations for loc and emits event for the
        View
        """
        self.add_normal_moves(loc)
        self.add_jump_moves(loc)
        self.post(CreateAvailableLocs(self.available_locations), Conf.VIEW)

    def remove_available_locs(self):
        """Remove available locations list.
        Method emits remove available locations to the view and removes the list
        """
        self.post(RemoveAvailableLocs(self.available_locations), Conf.VIEW)
        self.available_locations = []

    def is_valid_move(self, loc_end):
        """Move validation action.
        :param loc_end: location(model based) points where move will finish.
        :return int: 1 for valid and 0 for invalid
        Method checks if loc_end belongs to the list of available moves.
        """
        return loc_end in self.available_locations

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
                            if not new_loc in self.available_locations and \
                                    not new_loc == self.piece_selected_loc:
                                self.available_locations.append(new_loc)
                                self.add_jump_moves(new_loc)

    def set_ai_at_random(self):
        pass
        # ai_players = [0, 1]
    #
    # def not_move_own(self, loc):
    #     return self.board.get_field(loc) != self.current_player

    def not_free_field(self, loc):
        return self.board.get_field(loc) != 0

    def is_own_piece(self, loc):
        """Check if piece at loc belongs to current player.
        :param loc: location(model based) to check.
        :return int: 1 for valid and 0 for invalid
        Method gets the piece from the given location and
        compares it's value to current_player value
        """
        piece = self.board.get_field(loc)
        return piece.value == self.current_player

    def make_move(self, start_loc, end_loc):
        """Change actual model values for pieces stored.
        :param start_loc: location(model based).
        :param end_loc: location(model based).
        Method swaps pieces at given locations.
        """
        temp = self.board.get_field(start_loc)
        self.board.set_field(start_loc, self.board.get_field(end_loc))
        self.board.set_field(end_loc, temp)
        if Conf.DEBUG:
            self.board.print_board()

    def move(self, loc):
        """
        Moves selected piece to a location
        :param loc: location (model) to move to
        :return: None
        """
        # get piece uid
        uid = self.board.get_field(self.piece_selected_loc).uid
        # Update model
        self.make_move(self.piece_selected_loc, loc)
        # Deselect piece
        self.deselect_piece(self.piece_selected_loc)
        # Order view to update
        self.post(PieceMoveEvent(uid, loc), Conf.VIEW)
        # TODO: CHECK WIN?
        # Update current player
        self.next_player()

    def next_player(self):
        """ Firstly check if someone won, then updates current player
        to next player.Method increments current_player,
        if biggest player number is reached current player is set
        to first player.
        """
        if self.has_won(self.current_player):
            print str(self.current_player) + ' has won'
            Conf.WINNER = self.current_player
            self.post(SwitchScreenEvent(Conf.END_GAME), Conf.ALL)
        else:
            self.current_player_index += 1
            if self.current_player_index == len(self.players):
                self.current_player_index = 0
            self.current_player = self.ai_players[self.current_player_index]

    def is_ai_player(self, player):
        if self.ai_players.__contains__(player):
            return True
        return False

    def get_grid_dimensions(self):
        """
        Retrieves dimension of board grid as a tuple
        :return: tuple of dimensions for the board
        """
        return self.board.SIZE_BOARD_X_GRID, self.board.SIZE_BOARD_Y_GRID

    def get_pieces(self):
        """Retrieves board pieces.
        :return list: A list of Piece dict with piece coordinates.
        """
        pieces = []
        for y in range(self.board.SIZE_BOARD_Y_GRID):
            for x in range(self.board.SIZE_BOARD_X_GRID):
                field = self.board.get_field((x, y))
                if field.value != Conf.NON_PLAYABLE and field.value != Conf.EMPTY:
                    pieces.append({'x': x, 'y': y, 'piece': field})
        return pieces

    def get_board_grid(self):
        """Retrieves board places.
        :return list: A list of board places.
        """
        fields = []
        for y in range(self.board.SIZE_BOARD_Y_GRID):
            for x in range(self.board.SIZE_BOARD_X_GRID):
                field = self.board.get_field((x, y))
                if field.value != Conf.NON_PLAYABLE:
                    fields.append((x, y))
        return fields

    def has_won(self, player):
        for loc in self.board.win_sectors.get(player):
            if self.board.get_field(loc).value != player:
                return 0
        return 1


class DiamondGameModel(MVCObject):
    def __init__(self, ev_manager):
        MVCObject.__init__(self, ev_manager, '[GameModel]')
        self.ready = 0
        self.current_player = Conf.EMPTY
        self.size_player_triangle_base = 3
        self.board = DiamondBoard()
        self.number_of_players = 0
        self.current_player_index = 0
        self.players = []
        self.ai_players = []
        i = 1
        for key, value in Conf.OPT_OPTIONS.iteritems():
            if not key == Conf.AI_DIF and not key == Conf.BFIELDS\
                    and not key == Conf.BP4 and not key == Conf.BP5 and not key == Conf.BP6:
                if value > Conf.OPT_NONE:
                    self.number_of_players += 1
                    if value == Conf.OPT_AI:
                        self.ai_players.append(i)
                    self.players.append(i)
                i += 1
        self.set_ai_at_random()
        self.current_player = self.players[self.current_player_index]
        self.piece_selected = 0
        self.piece_selected_loc = (-1, -1)
        self.available_locations = []
        self.waiting_for_ai = 0
    # initialise game for players set with the board
    # ai players is the list of player positions that
    # indicates that a player at that position is managed by ai
    #
    # current player is set from 1..6 as defined in config

    def does_handle_event(self, event):
        return 1

    def handle_event(self, event):
        # Whenever View is ready provide pieces and board
        if isinstance(event, SubModulesLoadedEvent):
            # initiate the GAME
            if event.module == Conf.VIEW and event.sub_module == Conf.GAME2:
                self.board = DiamondBoard()
                self.post(BoardCreatedEvent(self.get_board_grid(), self.get_grid_dimensions()), Conf.VIEW)
                self.board.init_board(self.number_of_players)
                self.post(PiecesCreatedEvent(self.get_pieces()), Conf.VIEW)
                self.ready = 1
                # TODO: resize event
                if Conf.DEBUG:
                    print self.get_grid_dimensions()
        elif isinstance(event, GameObjectClickEvent):
            if event.typ == Conf.GAME_CONTROL:
                pass
                # music on/off
                # sound on/off
                # save/load
                # restart
            elif event.typ == Conf.GAME_PLAY:
                if self.is_ai_move():
                    return
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
                        self.reselect_piece(event.value)
                    elif self.is_valid_move(event.value):
                        # Piece movement
                        self.move(event.value)
                        self.deselect_piece(event.value)

                # select/deselect -> show/remove hints
                # move
                # undo move
        elif isinstance(event, TickEvent):
            if self.is_ai_move():
                if not self.waiting_for_ai and self.ready:
                    self.waiting_for_ai = 1
                    self.post(AIMakeMoveEvent(self.collect_data_for_ai()), Conf.AI)
        elif isinstance(event, AIMovedEvent):
            self.process_ai_move(event.data)
            self.waiting_for_ai = 0

    def is_ai_move(self):
        return self.current_player in self.ai_players

    def process_ai_move(self, data):
        if data['skip']:
            self.next_player()
        else:
            self.select_piece(data['start'])
            self.move(data['end'])
            self.deselect_piece(data['end'])

    def collect_data_for_ai(self):
        val = {'board': self.board, 'player': self.current_player}
        return val

    def select_piece(self, loc):
        """Piece select action.
        :param loc: location(model based).
        Method makes unique piece on the board selected
        stores location (m) of the selected piece
        and sets selected flag to true
        PieceSelectedEvent is emmited with piece unique id
        for the view to process.
        Also create a list of available locations and
        emit event with them.
        """
        self.piece_selected = 1
        self.piece_selected_loc = loc
        piece = self.board.get_field(loc)
        self.post(PieceSelectedEvent(piece.uid), Conf.VIEW)
        self.create_available_locs(loc)

    def deselect_piece(self, loc):
        """Piece select action.
        :param loc: location(model based).
        Method deselects selected piece
        sets selected flag to false and location to (-1, -1)
        PieceDeSelectedEvent is emmited with piece unique id
        for the view to process.
        Also remove list of available locations and
        emit event with them removed.
        """
        self.piece_selected = 0
        self.piece_selected_loc = (-1, -1)
        piece = self.board.get_field(loc)
        self.post(PieceDeSelectedEvent(piece.uid), Conf.VIEW)
        self.remove_available_locs()

    def reselect_piece(self, loc_yes):
        """Piece select action.
        :param loc_yes: location(model based) for selected piece.
        :param loc_no: location(model based) for deselected piece.
        Method deselects old piece and selects new piece emmiting
        corresponding PieceSelectedEvent and PieceDeSelectedEvent
        with pieces unique ids for the view to process.
        selected_piece_loc is updated to the new piece.
        Update available locations and emit event
        """
        loc_no = self.piece_selected_loc
        piece_yes = self.board.get_field(loc_yes)
        piece_no = self.board.get_field(loc_no)
        self.post(PieceDeSelectedEvent(piece_no.uid), Conf.VIEW)
        self.post(PieceSelectedEvent(piece_yes.uid), Conf.VIEW)
        self.piece_selected_loc = loc_yes
        self.remove_available_locs()
        self.create_available_locs(loc_yes)

    def create_available_locs(self, loc):
        """Create available locations list.
        :param loc: location(model based) points from where move will be started.
        Method creates list of reachable locations for loc and emits event for the
        View
        """
        self.add_normal_moves(loc)
        self.add_jump_moves(loc)
        self.post(CreateAvailableLocs(self.available_locations), Conf.VIEW)

    def remove_available_locs(self):
        """Remove available locations list.
        Method emits remove available locations to the view and removes the list
        """
        self.post(RemoveAvailableLocs(self.available_locations), Conf.VIEW)
        self.available_locations = []

    def is_valid_move(self, loc_end):
        """Move validation action.
        :param loc_end: location(model based) points where move will finish.
        :return int: 1 for valid and 0 for invalid
        Method checks if loc_end belongs to the list of available moves.
        """
        return loc_end in self.available_locations

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
                            if not new_loc in self.available_locations and \
                                    not new_loc == self.piece_selected_loc:
                                self.available_locations.append(new_loc)
                                self.add_jump_moves(new_loc)

    def set_ai_at_random(self):
        pass
        # ai_players = [0, 1]
    #
    # def not_move_own(self, loc):
    #     return self.board.get_field(loc) != self.current_player

    def not_free_field(self, loc):
        return self.board.get_field(loc) != 0

    def is_own_piece(self, loc):
        """Check if piece at loc belongs to current player.
        :param loc: location(model based) to check.
        :return int: 1 for valid and 0 for invalid
        Method gets the piece from the given location and
        compares it's value to current_player value
        """
        piece = self.board.get_field(loc)
        return piece.value == self.current_player

    def make_move(self, start_loc, end_loc):
        """Change actual model values for pieces stored.
        :param start_loc: location(model based).
        :param end_loc: location(model based).
        Method swaps pieces at given locations.
        """
        temp = self.board.get_field(start_loc)
        self.board.set_field(start_loc, self.board.get_field(end_loc))
        self.board.set_field(end_loc, temp)
        if Conf.DEBUG:
            self.board.print_board()

    def move(self, loc):
        """
        Moves selected piece to a location
        :param loc: location (model) to move to
        :return: None
        """
        # get piece uid
        uid = self.board.get_field(self.piece_selected_loc).uid
        # Update model
        self.make_move(self.piece_selected_loc, loc)
        # Deselect piece
        self.deselect_piece(self.piece_selected_loc)
        # Order view to update
        self.post(PieceMoveEvent(uid, loc), Conf.VIEW)
        # TODO: CHECK WIN?
        # Update current player
        self.next_player()

    def next_player(self):
        """ Firstly check if someone won, then updates current player
        to next player.Method increments current_player,
        if biggest player number is reached current player is set
        to first player.
        """
        if self.has_won(self.current_player):
            print str(self.current_player) + ' has won'
            Conf.WINNER = self.current_player
            self.post(SwitchScreenEvent(Conf.END_GAME), Conf.ALL)
        else:
            self.current_player_index += 1
            if self.current_player_index == len(self.players):
                self.current_player_index = 0
            self.current_player = self.ai_players[self.current_player_index]

    def is_ai_player(self, player):
        if self.ai_players.__contains__(player):
            return True
        return False

    def get_grid_dimensions(self):
        """
        Retrieves dimension of board grid as a tuple
        :return: tuple of dimensions for the board
        """
        return self.board.SIZE_BOARD_X_GRID, self.board.SIZE_BOARD_Y_GRID

    def get_pieces(self):
        """Retrieves board pieces.
        :return list: A list of Piece dict with piece coordinates.
        """
        pieces = []
        for y in range(self.board.SIZE_BOARD_Y_GRID):
            for x in range(self.board.SIZE_BOARD_X_GRID):
                field = self.board.get_field((x, y))
                if field.value != Conf.NON_PLAYABLE and field.value != Conf.EMPTY:
                    pieces.append({'x': x, 'y': y, 'piece': field})
        return pieces

    def get_board_grid(self):
        """Retrieves board places.
        :return list: A list of board places.
        """
        fields = []
        for y in range(self.board.SIZE_BOARD_Y_GRID):
            for x in range(self.board.SIZE_BOARD_X_GRID):
                field = self.board.get_field((x, y))
                if field.value != Conf.NON_PLAYABLE:
                    fields.append((x, y))
        return fields

    def has_won(self, player):
        for loc in self.board.win_sectors.get(player):
            if self.board.get_field(loc).value != player:
                return 0
        return 1

class OptionsModel(MVCObject):
    def __init__(self, ev_manager):
        MVCObject.__init__(self, ev_manager, '[model_options1]')

    def does_handle_event(self, event):
        return 1

    def handle_event(self, event):
        if isinstance(event, OptionsClickEvent):
            self.post(SwitchScreenEvent(event.value), Conf.ALL)


class CCOptionsModel(MVCObject):
    def __init__(self, ev_manager):
        MVCObject.__init__(self, ev_manager, '[model_options1]')
        self.options = {Conf.AI_DIF: [Conf.OPT_EASY, Conf.OPT_MEDIUM],
                        Conf.BP1: [Conf.OPT_NONE, Conf.OPT_HUMAN, Conf.OPT_AI],
                        Conf.BP2: [Conf.OPT_NONE, Conf.OPT_HUMAN, Conf.OPT_AI],
                        Conf.BP3: [Conf.OPT_NONE, Conf.OPT_HUMAN, Conf.OPT_AI],
                        Conf.BP4: [Conf.OPT_NONE, Conf.OPT_HUMAN, Conf.OPT_AI],
                        Conf.BP5: [Conf.OPT_NONE, Conf.OPT_HUMAN, Conf.OPT_AI],
                        Conf.BP6: [Conf.OPT_NONE, Conf.OPT_HUMAN, Conf.OPT_AI],
                        Conf.BFIELDS: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]}

        self.selected_options = {Conf.AI_DIF: Conf.OPT_OPTIONS.get(Conf.AI_DIF),
                                 Conf.BP1: Conf.OPT_OPTIONS.get(Conf.BP1),
                                 Conf.BP2: Conf.OPT_OPTIONS.get(Conf.BP2),
                                 Conf.BP3: Conf.OPT_OPTIONS.get(Conf.BP3),
                                 Conf.BP4: Conf.OPT_OPTIONS.get(Conf.BP4),
                                 Conf.BP5: Conf.OPT_OPTIONS.get(Conf.BP5),
                                 Conf.BP6: Conf.OPT_OPTIONS.get(Conf.BP6),
                                 Conf.BFIELDS: Conf.OPT_OPTIONS.get(Conf.BFIELDS)}

    def does_handle_event(self, event):
        return 1

    def handle_event(self, event):
        if isinstance(event, OptionsClickEvent):
            id = event.value
            a = self.selected_options.get(id)
            lst = self.options.get(id)
            if len(lst) == a+1:
                self.selected_options[id] = 0
            else:
                self.selected_options[id] = a+1
            Conf.OPT_OPTIONS[id] = self.selected_options[id]
            self.post(OptionButtonStateChangeEvent(id, self.selected_options[id]), Conf.VIEW)


class EndGameModel(MVCObject):
    def __init__(self, ev_manager):
        MVCObject.__init__(self, ev_manager, '[model_options1]')

    def does_handle_event(self, event):
        return 1

    def handle_event(self, event):
        if isinstance(event, OptionsClickEvent):
            self.post(SwitchScreenEvent(event.value), Conf.ALL)


class DOptionsModel(MVCObject):
    def __init__(self, ev_manager):
        MVCObject.__init__(self, ev_manager, '[model_options1]')
        self.options = {Conf.AI_DIF: [Conf.OPT_EASY, Conf.OPT_MEDIUM],
                        Conf.BP1: [Conf.OPT_NONE, Conf.OPT_HUMAN, Conf.OPT_AI],
                        Conf.BP2: [Conf.OPT_NONE, Conf.OPT_HUMAN, Conf.OPT_AI],
                        Conf.BP3: [Conf.OPT_NONE, Conf.OPT_HUMAN, Conf.OPT_AI]}

        self.selected_options = {Conf.AI_DIF: Conf.OPT_OPTIONS.get(Conf.AI_DIF),
                                 Conf.BP1: Conf.OPT_OPTIONS.get(Conf.BP1),
                                 Conf.BP2: Conf.OPT_OPTIONS.get(Conf.BP2),
                                 Conf.BP3: Conf.OPT_OPTIONS.get(Conf.BP3)}

    def does_handle_event(self, event):
        return 1

    def handle_event(self, event):
        if isinstance(event, OptionsClickEvent):
            id = event.value
            a = self.selected_options.get(id)
            lst = self.options.get(id)
            if len(lst) == a+1:
                self.selected_options[id] = 0
            else:
                self.selected_options[id] = a+1
            Conf.OPT_OPTIONS[id] = self.selected_options[id]
            self.post(OptionButtonStateChangeEvent(id, self.selected_options[id]), Conf.VIEW)


class Board(object):
    """
    Board class. Board can be customized to:
        - How many players will play (2-6)
        - What is the size of player triangle: hence how many pieces he has

    To resize board new instance should be created with desired size

    To change number of players - reinitiate the board with desired number of players
    """

    # creates empty board
    def __init__(self, size_player_base=4):
        self.SIZE_PLAYER_BASE = size_player_base
        self.SIZE_PLAYER_BASE_GRID = (self.SIZE_PLAYER_BASE * 2) - 1
        self.SIZE_BOARD_CENTER = self.SIZE_PLAYER_BASE + 1
        self.SIZE_TRIANGLE_BASE = (self.SIZE_PLAYER_BASE * 3) + 1
        self.SIZE_BOARD_X_GRID = (self.SIZE_TRIANGLE_BASE * 2) - 1
        self.SIZE_BOARD_Y_GRID = (self.SIZE_PLAYER_BASE * 4) + 1
        self.board = []
        self.win_sectors = {Conf.P1: [], Conf.P2: [], Conf.P3: [],
                            Conf.P4: [], Conf.P5: [], Conf.P6: []}
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
        margin_left = []
        margin_right = []
        for i in range(cnt_non_playable):
            margin_left.append(Piece(Conf.NON_PLAYABLE))
        for i in range(cnt_non_playable):
            margin_right.append(Piece(Conf.NON_PLAYABLE))
        center = []
        for i in range(1, num_fields + empties + 1):
            if i % 2 == 0:
                center.append(Piece(Conf.NON_PLAYABLE))
            else:
                center.append(Piece(Conf.EMPTY))
        return margin_left + center + margin_right

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
    def init_board(self, num_players=3):
        self.make_board()
        a1 = 1 if Conf.OPT_OPTIONS.get(Conf.BP1) > 0 else 0
        a2 = 2 if Conf.OPT_OPTIONS.get(Conf.BP2) > 0 else 0
        a3 = 3 if Conf.OPT_OPTIONS.get(Conf.BP3) > 0 else 0
        a4 = 4 if Conf.OPT_OPTIONS.get(Conf.BP4) > 0 else 0
        a5 = 5 if Conf.OPT_OPTIONS.get(Conf.BP5) > 0 else 0
        a6 = 6 if Conf.OPT_OPTIONS.get(Conf.BP6) > 0 else 0
        players = [a1, a3, a6, a5, a4, a2]
        i = self.SIZE_PLAYER_BASE_GRID
        for y in range(self.SIZE_BOARD_Y_GRID):
            row = self.board[y]
            if y/self.SIZE_PLAYER_BASE == 0:
                for x in range(self.SIZE_BOARD_X_GRID):
                    if row[x].value == 0:
                        row[x] = Piece(players[0])
                        self.win_sectors.get(Conf.P2).append((x, y))
            elif y/self.SIZE_PLAYER_BASE == 1:
                for x in range(self.SIZE_BOARD_X_GRID):
                    if row[x].value == 0:
                        if x < i:
                            row[x] = Piece(players[1])
                            self.win_sectors.get(Conf.P4).append((x, y))
                        elif x + i >= self.SIZE_BOARD_X_GRID:
                            row[x] = Piece(players[2])
                            self.win_sectors.get(Conf.P5).append((x, y))
                i -= 1
            elif (y-1)/self.SIZE_PLAYER_BASE == 2:
                i += 1
                for x in range(self.SIZE_BOARD_X_GRID):
                    if row[x].value == 0:
                        if x < i:
                            row[x] = Piece(players[3])
                            self.win_sectors.get(Conf.P6).append((x, y))
                        elif x + i >= self.SIZE_BOARD_X_GRID:
                            row[x] = Piece(players[4])
                            self.win_sectors.get(Conf.P3).append((x, y))
            elif (y-1)/self.SIZE_PLAYER_BASE == 3:
                for x in range(self.SIZE_BOARD_X_GRID):
                    if row[x].value == 0:
                        row[x] = Piece(players[5])
                        self.win_sectors.get(Conf.P1).append((x, y))
        if Conf.DEBUG:
            self.print_board()

    # for debug purposes
    def print_board(self):
        line = ''
        for y in range(self.SIZE_BOARD_Y_GRID):
            for x in range(self.SIZE_BOARD_X_GRID):
                if self.board[y][x].value == -1:
                    line += '_'
                elif self.board[y][x].value == 0:
                    line += 'x'
                else:
                    line += str(self.board[y][x].value)
            print line
            line = ''

        ba1 = []
        ba2 = []
        ba3 = []
        ba4 = []
        ba5 = []
        ba6 = []
        for y in range(self.SIZE_BOARD_Y_GRID):
            for x in range(self.SIZE_BOARD_X_GRID):
                if self.board[y][x].value == 1:
                    ba1.append((x, y))
                elif self.board[y][x].value == 2:
                    ba2.append((x, y))
                elif self.board[y][x].value == 3:
                    ba3.append((x, y))
                elif self.board[y][x].value == 4:
                    ba4.append((x, y))
                elif self.board[y][x].value == 5:
                    ba5.append((x, y))
                elif self.board[y][x].value == 6:
                    ba6.append((x, y))
        print ba1
        print ba2
        print ba3
        print ba4
        print ba5
        print ba6


class DiamondBoard(object):
    """
    Board class. Board can be customized to:
        - How many players will play (2-6)
        - What is the size of player triangle: hence how many pieces he has

    To resize board new instance should be created with desired size

    To change number of players - reinitiate the board with desired number of players
    """

    # creates empty board
    def __init__(self):
        self.SIZE_PLAYER_BASE = 3
        self.SIZE_PLAYER_BASE_GRID = (self.SIZE_PLAYER_BASE * 2) - 1
        self.SIZE_BOARD_CENTER = self.SIZE_PLAYER_BASE + 1
        self.SIZE_TRIANGLE_BASE = (self.SIZE_PLAYER_BASE * 3) + 1
        self.SIZE_BOARD_X_GRID = (self.SIZE_TRIANGLE_BASE * 2) - 1
        self.SIZE_BOARD_Y_GRID = (self.SIZE_PLAYER_BASE * 4) + 1
        self.board = []
        self.win_sectors = {Conf.P1: [], Conf.P2: [], Conf.P3: [],
                            Conf.P4: [], Conf.P5: [], Conf.P6: []}
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
        margin_left = []
        margin_right = []
        for i in range(cnt_non_playable):
            margin_left.append(Piece(Conf.NON_PLAYABLE))
        for i in range(cnt_non_playable):
            margin_right.append(Piece(Conf.NON_PLAYABLE))
        center = []
        for i in range(1, num_fields + empties + 1):
            if i % 2 == 0:
                center.append(Piece(Conf.NON_PLAYABLE))
            else:
                center.append(Piece(Conf.EMPTY))
        return margin_left + center + margin_right

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
    def init_board(self, num_players=3):
        self.make_board()
        a1 = 1 if Conf.OPT_OPTIONS.get(Conf.BP1) > 0 else 0
        a2 = 2 if Conf.OPT_OPTIONS.get(Conf.BP2) > 0 else 0
        a3 = 3 if Conf.OPT_OPTIONS.get(Conf.BP3) > 0 else 0

        p1 = [(9, 0), (8, 1), (10, 1), (7, 2), (9, 2), (11, 2), (6, 3), (8, 3), (10, 3), (12,3)]
        p1_win = [(6, 9), (8, 9), (10, 9), (12,9), (7, 10), (9, 10), (11, 10), (8, 11), (10, 11), (9, 12)]


        p3_win = [(0, 3), (2, 3), (4, 3), (6, 3), (1, 4), (3, 4), (5, 4), (2, 5), (4, 5), (3, 6)]
        p3 = [(15, 6), (14, 7), (16, 7), (13, 8), (15, 8), (17, 8), (12, 9), (14, 9), (16, 9), (18, 9)]

        p2 = [(3, 6), (2, 7), (4, 7), (1, 8), (3, 8), (5, 8), (0, 9), (2, 9), (4, 9), (6, 9)]
        p2_win = [(12, 3), (14, 3), (16, 3), (18, 3), (13, 4), (15, 4), (17, 4), (14, 5), (16, 5), (15, 6)]

        if a1 == 1:
            for loc in p1:
                self.board[loc[1]][loc[0]] = Piece(1)
            self.win_sectors[1] = p1_win
        if a2 == 2:
            for loc in p2:
                self.board[loc[1]][loc[0]] = Piece(2)
            self.win_sectors[2] = p2_win
        if a3 == 3:
            for loc in p3:
                self.board[loc[1]][loc[0]] = Piece(3)
            self.win_sectors[3] = p3_win

        if Conf.DEBUG:
            self.print_board()

    # for debug purposes
    def print_board(self):
        line = ''
        for y in range(self.SIZE_BOARD_Y_GRID):
            for x in range(self.SIZE_BOARD_X_GRID):
                if self.board[y][x].value == -1:
                    line += '_'
                elif self.board[y][x].value == 0:
                    line += 'x'
                else:
                    line += str(self.board[y][x].value)
            print line
            line = ''

        ba1 = []
        ba2 = []
        ba3 = []
        ba4 = []
        ba5 = []
        ba6 = []
        for y in range(self.SIZE_BOARD_Y_GRID):
            for x in range(self.SIZE_BOARD_X_GRID):
                if self.board[y][x].value == 1:
                    ba1.append((x, y))
                elif self.board[y][x].value == 2:
                    ba2.append((x, y))
                elif self.board[y][x].value == 3:
                    ba3.append((x, y))
                elif self.board[y][x].value == 4:
                    ba4.append((x, y))
                elif self.board[y][x].value == 5:
                    ba5.append((x, y))
                elif self.board[y][x].value == 6:
                    ba6.append((x, y))
        print ba1
        print ba2
        print ba3
        print ba4
        print ba5
        print ba6


class Piece(object):
    count = 0

    def __init__(self, val):
        """
        Creates a piece with unique id value and its 'player' value
        :param val: player number
        :return: nothing
        """
        object.__init__(self)
        Piece.count += 1
        self.value = val
        self.uid = Piece.count
        # if Conf.DEBUG:
        #     print(self)

    def __str__(self):
        return str(self.uid) + ': ' + str(self.value)

    def __repr__(self):
        return self.__str__()

if __name__ == "__main__":
    raise Exception("Unexpected")
