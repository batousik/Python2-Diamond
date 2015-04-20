import os
import pygame
from pygame.constants import RLEACCEL


class Utils(object):
    def __init__(self):
        pass

    @staticmethod
    def load_image(name, colorkey=None):
        fullname = os.path.join('img', name)
        try:
            image = pygame.image.load(fullname)
        except pygame.error, message:
            print 'Cannot load image:', name
            raise SystemExit, message
        image = image.convert()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, RLEACCEL)
        return image, image.get_rect()

    @staticmethod
    def load_sound(name):
        if not pygame.mixer:
            return NoneSound()
        fullname = os.path.join('data', name)
        try:
            sound = pygame.mixer.Sound(fullname)
        except pygame.error, message:
            print 'Cannot load sound:', wav
            raise SystemExit, message
        return sound


class NoneSound:
    def __init__(self):
        pass

    def play(self):
                pass