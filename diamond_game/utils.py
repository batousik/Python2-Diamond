import os
import pygame
from pygame.constants import RLEACCEL


class Utils(object):
    def __init__(self):
        pass

    @staticmethod
    def load_image(name, colorkey=None):
        fullname = os.path.join('img', name) + '.png'
        try:
            image = pygame.image.load(fullname)
        except pygame.error, message:
            print 'Cannot load image: ', name
            raise SystemExit(message)
        image = image.convert_alpha()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, RLEACCEL)
        return image

    @staticmethod
    def load_sound(name):
        if not pygame.mixer:
            return NoneSound()
        fullname = os.path.join('data', name)
        try:
            sound = pygame.mixer.Sound(fullname)
        except pygame.error, message:
            print 'Cannot load sound:'
            raise SystemExit(message)
        return sound

    @staticmethod
    def load_all_sounds():
        if not pygame.mixer:
            return NoneSound()
        sounds = {}
        for filename in os.listdir('sounds'):
            filename_no_ext = filename[:-4]
            fullname = os.path.join('sounds', filename)
            try:
                sound = pygame.mixer.Sound(fullname)
                sounds[filename_no_ext] = sound
            except pygame.error, message:
                print 'Cannot load sound:'
                raise SystemExit(message)
        return sounds


class NoneSound:
    def __init__(self):
        pass

    def play(self):
                pass