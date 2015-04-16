import math


class Conf(object):
    non_playable = -1
    empty = 0
    p1 = 1
    p2 = 2
    p3 = 3
    p4 = 4
    p5 = 5
    p6 = 6

    # Colours
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    dark_red = (100, 0, 0)
    dark_blue = (0, 0, 100)
    dark_green = (0, 100, 0)
    white = (255, 255, 255)
    black = (0, 0, 0)

    colours = [white, red, green, blue, dark_red, dark_blue, dark_green, black]

    # Game settings
    default_size_player_base = 4

    # Views
    screen_size = 400, 400

    # Game View
    piece_rad = 10
    piece_size = piece_rad * 2
    y_separation = int(math.sin(math.pi/3) * piece_rad)

    # Menu View
    b1_loc = screen_size[0]/2, screen_size[0]/2 - 30
    b2_loc = screen_size[0]/2, screen_size[0]/2
    b3_loc = screen_size[0]/2, screen_size[0]/2 + 30

    @staticmethod
    def loc_to_view(x, y):
        return x * Conf.piece_size + Conf.piece_rad, y * (Conf.piece_size+Conf.y_separation) + Conf.piece_rad

    @staticmethod
    def loc_to_model(x, y):
        return x / Conf.piece_size, y / (Conf.piece_size+Conf.y_separation)
