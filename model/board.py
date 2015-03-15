SIZE_PLAYER_BASE = 10
SIZE_PLAYER_BASE_GRID = (SIZE_PLAYER_BASE * 2) - 1
SIZE_BOARD_CENTER = SIZE_PLAYER_BASE + 1
SIZE_TRIANGLE_BASE = (SIZE_PLAYER_BASE * 3) + 1
SIZE_TRIANGLE_BASE_GRID = (SIZE_TRIANGLE_BASE * 2) - 1
SIZE_BOARD_X_GRID = (SIZE_TRIANGLE_BASE * 2) - 1
SIZE_BOARD_Y_GRID = (SIZE_PLAYER_BASE * 4) + 1


def mrow(num_fields):
    empties = num_fields-1
    non_playable = (SIZE_BOARD_X_GRID - num_fields - empties)/2
    margin = [-1] * non_playable
    center = []
    for i in range(1, num_fields + empties + 1):
        if i % 2 == 0:
            center.append(-1)
        else:
            center.append(0)
    return margin + center + margin


def make_board():
    board = []
    cnt = 0
    last_ind = 0

    for i in range(1, SIZE_BOARD_Y_GRID+1):
        if i/SIZE_BOARD_CENTER == 0:
            board.append(mrow(i))
        elif i/SIZE_BOARD_CENTER == 1:
            board.append(mrow(SIZE_TRIANGLE_BASE-cnt))
            cnt += 1
            last_ind = len(board) - 1
        else:
            last_ind -= 1
            board.append(list(board[last_ind]))

    return board


def init_board(board):
    i = SIZE_PLAYER_BASE_GRID
    for y in range(SIZE_BOARD_Y_GRID):
        row = board[y]
        if y/SIZE_PLAYER_BASE == 0:
            for x in range(SIZE_BOARD_X_GRID):
                if row[x] == 0:
                    row[x] = 1
        elif y/SIZE_PLAYER_BASE == 1:
            for x in range(SIZE_BOARD_X_GRID):
                if row[x] == 0:
                    if x < i:
                        row[x] = 2
                    elif x + i >= SIZE_TRIANGLE_BASE_GRID:
                        row[x] = 3
            i -= 1
        elif (y-1)/SIZE_PLAYER_BASE == 2:
            i += 1
            for x in range(SIZE_BOARD_X_GRID):
                if row[x] == 0:
                    if x < i:
                        row[x] = 4
                    elif x + i >= SIZE_TRIANGLE_BASE_GRID:
                        row[x] = 5

        elif (y-1)/SIZE_PLAYER_BASE == 3:
            for x in range(SIZE_BOARD_X_GRID):
                if row[x] == 0:
                    row[x] = 6

    return board


def print_board(board):
    line = ''
    for y in range(SIZE_BOARD_Y_GRID):
        for x in range(SIZE_BOARD_X_GRID):
            if board[y][x] == -1:
                line += '_'
            elif board[y][x] == 0:
                line += 'x'
            else:
                line += str(board[y][x])
        print line
        line = ''


if __name__ == "__main__":
    print "Hello Diamond Model"
    # print (27/4)
    # print_board()
    # print get_row(12)
    # print len(get_row(7))
    # print_board(make_board())

    print_board(init_board(make_board()))
