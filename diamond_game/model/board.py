from diamond_game.config import Conf

'''
This module contains class board. Board can be customized to:
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
    print "Hello Diamond Model"
    board = Board(12)
    board.init_board(5)
    board.print_board()