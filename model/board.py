SIZE_PLAYER_BASE = 4
SIZE_BOARD_CENTER = SIZE_PLAYER_BASE + 1
SIZE_TRIANGLE_BASE = (SIZE_PLAYER_BASE * 3) + 1
SIZE_BOARD_X = (SIZE_TRIANGLE_BASE * 2) - 1
SIZE_BOARD_Y = (SIZE_PLAYER_BASE * 4) + 1


# def init_board():
#     for y in (0, BOARD_SIZE_Y):
#         for x in (0, BOARD_SIZE_X):
#             board[y][x]


def mrow(num_fields):
    empties = num_fields-1
    non_playable = (SIZE_BOARD_X - num_fields - empties)/2
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

    for i in range(1, SIZE_BOARD_Y+1):
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


# def init_board(board):
#     for i in range(SIZE_BOARD_Y):
#         row = board[i]
#         if i/SIZE_BOARD_CENTER == 0:
#             board.append(mrow(i))
#         elif i/SIZE_BOARD_CENTER == 1:
#             board.append(mrow(SIZE_TRIANGLE_BASE-cnt))
#             cnt += 1
#             last_ind = len(board) - 1
#         else:
#             last_ind -= 1
#             board.append(list(board[last_ind]))

def print_board(board):
    line = ''
    for y in range(SIZE_BOARD_Y):
        for x in range(SIZE_BOARD_X):
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

    print_board(make_board())
