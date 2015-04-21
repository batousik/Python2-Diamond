import math


class Conf(object):
    """
    Class for various constants required for the program
    """
    # Debug mode on/off 1/0
    DEBUG = 1
    # Program constants
    ALL = 1
    MODEL = 2
    VIEW = 3
    CONTROLLER = 4
    SOUND = 41
    AI = 42

    MENU = 5
    OPTIONS = 6
    GAME = 7
    GAME2 = 1024
    END_GAME = 87

    EXIT = 99

    GAME_PLAY = 50
    GAME_CONTROL = 51

    LOCK_ACTION = 1
    UNLOCK_ACTION = 0

    debug_dict = {1: 'ALL', 2: 'MODEL', 3: 'VIEW',
                  4: 'CONTROLLER', 5: 'MENU',
                  6: 'OPTIONS', 7: 'GAME',
                  99: 'EXIT', 41: 'SOUND',
                  42: 'AI', 87: 'END_GAME',
                  1024: 'GAMEDIAMOND'}

    # Board constants
    NON_PLAYABLE = -1
    EMPTY = 0
    P1 = 1
    P2 = 2
    P3 = 3
    P4 = 4
    P5 = 5
    P6 = 6

    DIRECTION_UP_LEFT = (-1, -1)
    DIRECTION_UP_RIGHT = (1, -1)
    DIRECTION_DOWN_LEFT = (-1, 1)
    DIRECTION_DOWN_RIGHT = (1, 1)
    DIRECTION_LEFT = (-2, 0)
    DIRECTION_RIGHT = (2, 0)

    DIRECTION_DOUBLE_UP_LEFT = (-2, -2)
    DIRECTION_DOUBLE_UP_RIGHT = (2, -2)
    DIRECTION_DOUBLE_DOWN_LEFT = (-2, 2)
    DIRECTION_DOUBLE_DOWN_RIGHT = (2, 2)
    DIRECTION_DOUBLE_LEFT = (-4, 0)
    DIRECTION_DOUBLE_RIGHT = (4, 0)

    JUMP_DIRECTIONS = [DIRECTION_DOUBLE_UP_LEFT, DIRECTION_DOUBLE_UP_RIGHT,
                       DIRECTION_DOUBLE_DOWN_LEFT, DIRECTION_DOUBLE_DOWN_RIGHT,
                       DIRECTION_DOUBLE_LEFT, DIRECTION_DOUBLE_RIGHT]

    NORMAL_DIRECTIONS = [DIRECTION_UP_LEFT, DIRECTION_UP_RIGHT,
                         DIRECTION_DOWN_LEFT, DIRECTION_DOWN_RIGHT,
                         DIRECTION_LEFT, DIRECTION_RIGHT]

    # Colours
    COL_RED = (255, 0, 0)
    COL_GREEN = (0, 255, 0)
    COL_BLUE = (0, 0, 255)
    COL_DARK_RED = (100, 0, 0)
    COL_DARK_BLUE = (0, 0, 100)
    COL_DARK_GREEN = (0, 100, 0)
    COL_WHITE = (255, 255, 255)
    COL_BLACK = (0, 0, 0)

    COLOURS = [COL_WHITE, COL_RED, COL_GREEN, COL_BLUE, COL_DARK_RED, COL_DARK_BLUE, COL_DARK_GREEN, COL_BLACK]

    # Views
    SCREEN_SIZE = 800, 600

    # Game View
    PIECE_RAD = 5
    PIECE_SIZE = PIECE_RAD * 2
    X_SEPARATION = PIECE_SIZE
    Y_SEPARATION = int(math.sin(math.pi/3) * X_SEPARATION)
    BOARD_X_OFFSET = 30
    BOARD_Y_OFFSET = 30
    BOARD_CENTER = 300, 300
    PIECE_SLOW = 1
    PIECE_FAST = 10
    BOARD_LOC = BOARD_X_OFFSET, BOARD_Y_OFFSET
    BOARD_INNER_RAD = 230
    BOARD_INNER_OFFSET_X = 46
    BOARD_INNER_OFFSET_Y = 49
    BOARD_REAL_CENTER = BOARD_X_OFFSET+BOARD_INNER_OFFSET_X+BOARD_INNER_RAD, BOARD_Y_OFFSET+BOARD_INNER_OFFSET_Y+BOARD_INNER_RAD
    BOARD_RADIUS = 230
    BOARD_X_MARGIN = 27
    BOARD_Y_MARGIN = 40
    TOP_LEFT_POINT = 300 - 230 * math.cos(math.pi/3), 300 - 230 * math.sin(math.pi/3),
    PIECES_WIDTH = 2 * 230 * math.cos(math.pi/3)
    AMOUNT_X = 1
    AMOUNT_Y = 1

    # Menu View
    B1_LOC = SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2 - 80
    B2_LOC = SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2
    B3_LOC = SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2 + 80

    # Menu Options
    B_OPT_1_0 = B1_LOC
    DIAMOND = 1
    B_OPT_1_1 = B2_LOC
    CHINESE_CHECKERS = 2

    # @staticmethod
    # def loc_to_view(x, y):
    #     x_separation = (Conf.PIECE_WIDTH/Conf.AMOUNT_X)/4
    #     y_separation = int(math.sin(math.pi/3) * x_separation)
    #     Conf.PIECE_RAD = x_separation / 2
    #     Conf.PIECE_SIZE = x_separation
    #     new_x = Conf.BOARD_X_OFFSET + Conf.BOARD_X_MARGIN + x * Conf.PIECE_SIZE
    #     new_y = Conf.BOARD_Y_OFFSET + Conf.BOARD_Y_MARGIN + y * (Conf.PIECE_SIZE + y_separation)
    #     return new_x, new_y
    #
    # @staticmethod
    # def loc_to_model(x, y):
    #     new_x = x / Conf.PIECE_SIZE - (Conf.BOARD_X_OFFSET + Conf.BOARD_X_MARGIN)
    #     new_y = y / (Conf.PIECE_SIZE+Conf.Y_SEPARATION) - (Conf.BOARD_X_OFFSET + Conf.BOARD_Y_MARGIN)
    #     return new_x, new_y

    # Game options
    # DEFAULT_SIZE_PLAYER_BASE = 2
    NUM_PLAYERS = 6
    NUM_AI_PLAYERS = 0
    WINNER = 0

    AI_DIF = 200
    BP1 = 201
    BP2 = 202
    BP3 = 203
    BP4 = 204
    BP5 = 205
    BP6 = 206
    BFIELDS = 207

    OPT_OPTIONS = {BFIELDS: 5, AI_DIF: 1, BP1: 2, BP2: 2, BP3: 2,
                   BP4: 0, BP5: 0, BP6: 0}

    OPT_EASY = 0
    OPT_MEDIUM = 1
    OPT_NONE = 0
    OPT_HUMAN = 1
    OPT_AI = 2

    GAME_CHOSEN = CHINESE_CHECKERS

if __name__ == "__main__":
    raise Exception("Unexpected")
