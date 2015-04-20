# -*- coding: utf-8 -*-
import pygame
import time
from diamond_game import *


def main():
    # load pygame modules
    pygame.init()

    # check for sound and fonts support
    if not pygame.font:
        print 'Warning, fonts disabled'
    if not pygame.mixer:
        print 'Warning, sound disabled'

    # Instantiate EventManager object that manages
    # M-V-C Framework events
    event_manager = EventManager()

    controller_thread = MasterController(event_manager)
    view_thread = MasterView(event_manager)
    model_thread = MasterModel(event_manager)

    model_thread.start()
    controller_thread.start()
    view_thread.start()

    # The main game loop :)
    while controller_thread.is_alive() or view_thread.is_alive() \
            or model_thread.is_alive():
        time.sleep(0.03)  # ~33 FPS
        event_manager.post(TickEvent(), Conf.VIEW)
        pygame.event.pump()  # keeps pygame modules going

    # Has to be last line printed out
    print '_____END_____'

if __name__ == "__main__":
    main()
