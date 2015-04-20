import math


class Conf(object):
    # Debug mode on/off 1/0
    DEBUG = 1
    # Program constants
    ALL = 1
    MODEL = 2
    VIEW = 3
    CONTROLLER = 4

    MENU = 5
    OPTIONS = 6
    GAME = 7

    EXIT = 99

    GAME_PLAY = 50
    GAME_CONTROL = 51

    LOCK_ACTION = 1
    UNLOCK_ACTION = 0

    debug_dict = {1: 'ALL', 2: 'MODEL', 3: 'VIEW',
                  4: 'CONTROLLER', 5: 'MENU',
                  6: 'OPTIONS', 7: 'GAME',
                  99: 'EXIT'}

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

    # Game settings
    DEFAULT_SIZE_PLAYER_BASE = 4

    # Views
    SCREEN_SIZE = 800, 600

    # Game View
    PIECE_RAD = 10
    PIECE_SIZE = PIECE_RAD * 2
    Y_SEPARATION = int(math.sin(math.pi/3) * PIECE_RAD)
    BOARD_X_OFFSET = 0
    BOARD_Y_OFFSET = 0
    PIECE_SLOW = 1
    PIECE_FAST = 10

    # Menu View
    B1_LOC = SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2 - 80
    B2_LOC = SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2
    B3_LOC = SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2 + 80

    @staticmethod
    def loc_to_view(x, y):
        return x * Conf.PIECE_SIZE + Conf.PIECE_RAD, y * (Conf.PIECE_SIZE+Conf.Y_SEPARATION) + Conf.PIECE_RAD

    @staticmethod
    def loc_to_model(x, y):
        return x / Conf.PIECE_SIZE, y / (Conf.PIECE_SIZE+Conf.Y_SEPARATION)

    # Game options
    NUM_PLAYERS = 2
    NUM_AI_PLAYERS = 2


if __name__ == "__main__":
    raise Exception("Unexpected")
