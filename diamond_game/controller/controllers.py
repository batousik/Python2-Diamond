import traceback
import pygame
from pygame.constants import *
import sys
from diamond_game import *


class MasterController(MVCObject):
    def __init__(self, ev_manager):
        MVCObject.__init__(self, ev_manager, '[controller]')
        self.id = Conf.CONTROLLER
        self.sub_classes = {Conf.MENU: [MenuController],
                            Conf.GAME: [GameController],
                            Conf.GAME2: [GameController],
                            Conf.OPTIONS: [OptionsController],
                            Conf.CHINESE_CHECKERS: [ChineseCheckersOptionsController],
                            Conf.DIAMOND: [DiamondOptionsController],
                            Conf.END_GAME: [EndGameController]}
        self.switch_sub_modules(Conf.MENU)

    @property
    def get_next_event(self):
        return self.event_manager.get_next_controller_event()

    # noinspection PyBroadException
    def run(self):
        running = 1
        try:
            while running:
                # Check controller's event queue
                event = self.get_next_event
                # Handle events
                # If quit event then terminate
                if isinstance(event, QuitEvent):
                    print self.thread_name + ' is shutting down'
                    running = 0
                elif isinstance(event, SwitchScreenEvent):
                    # Switch sub_modules on request
                    self.switch_sub_modules(event.value)
                for py_game_event in pygame.event.get():
                    # Handle PyGame events
                    # Game end event
                    if py_game_event.type == QUIT:
                        # Send quit event and Terminate Controller
                        cur_event = QuitEvent()
                        self.post(cur_event, Conf.ALL)
                    else:
                        # find if a sub_module can handle the event
                        for a_controller in self.sub_modules:
                            # Look for a controller that accepts event
                            if a_controller.does_handle_event(py_game_event):
                                # Let controller handle event
                                a_controller.handle_py_game_event(py_game_event)
                                # Stop other controllers from handling current event
                                break
        except:
            e = sys.exc_info()[0]
            print '>>>>>>>>>>> Fatal Error in: ' + self.thread_name
            print e
            traceback.print_exc()
            self.post(QuitEvent(), Conf.ALL)


class MenuController(MVCObject):
    def __init__(self, ev_manager):
        MVCObject.__init__(self, ev_manager, '[MenuController]')

    def does_handle_event(self, event):
        if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN or event.type == MOUSEMOTION:
            return 1
        return 0

    def handle_py_game_event(self, event):
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            self.post(QuitEvent(), Conf.ALL)
        elif event.type == KEYDOWN and event.key == K_UP:
            self.post(MenuPrevEvent(), Conf.MODEL)
        elif event.type == KEYDOWN and event.key == K_DOWN:
            self.post(MenuNextEvent(), Conf.MODEL)
        elif event.type == KEYDOWN and (event.key == K_RETURN or event.key == K_SPACE):
            self.post(SoundPlayEvent('menu_click'), Conf.SOUND)
            self.post(MenuPressEvent(), Conf.MODEL)
        elif event.type == MOUSEBUTTONDOWN:
            button = event.button
            if button == 1:
                self.post(MouseClickEvent(event.pos), Conf.VIEW)
        elif event.type == MOUSEMOTION:
            self.post(MouseMotionEvent(event.pos), Conf.VIEW)


class GameController(MVCObject):
    def __init__(self, ev_manager):
        MVCObject.__init__(self, ev_manager, '[GameController]')

    def does_handle_event(self, event):
        if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN or event.type == MOUSEMOTION:
            return 1
        return 0

    def handle_py_game_event(self, event):
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            self.post(SwitchScreenEvent(Conf.MENU), Conf.ALL)
        elif event.type == MOUSEBUTTONDOWN:
            button = event.button
            if button == 1:
                self.post(MouseClickEvent(event.pos), Conf.VIEW)


class OptionsController(MVCObject):
    def __init__(self, ev_manager):
        MVCObject.__init__(self, ev_manager, '[model_options_1]')

    def does_handle_event(self, event):
        if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN or event.type == MOUSEMOTION:
            return 1
        return 0

    def handle_py_game_event(self, event):
        cur_event = None
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            cur_event = SwitchScreenEvent(Conf.MENU)
            self.event_manager.post(cur_event, Conf.ALL)
        elif event.type == MOUSEBUTTONDOWN:
            button = event.button
            if button == 1:
                cur_event = MouseClickEvent(event.pos)
                self.event_manager.post(cur_event, Conf.VIEW)


class ChineseCheckersOptionsController(MVCObject):
    def __init__(self, ev_manager):
        MVCObject.__init__(self, ev_manager, '[contr_options_cc]')

    def does_handle_event(self, event):
        if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN or event.type == MOUSEMOTION:
            return 1
        return 0

    def handle_py_game_event(self, event):
        cur_event = None
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            cur_event = SwitchScreenEvent(Conf.MENU)
            self.event_manager.post(cur_event, Conf.ALL)
        elif event.type == MOUSEBUTTONDOWN:
            button = event.button
            if button == 1:
                cur_event = MouseClickEvent(event.pos)
                self.event_manager.post(cur_event, Conf.VIEW)


class DiamondOptionsController(MVCObject):
    def __init__(self, ev_manager):
        MVCObject.__init__(self, ev_manager, '[contr_options_d]')

    def does_handle_event(self, event):
        if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN or event.type == MOUSEMOTION:
            return 1
        return 0

    def handle_py_game_event(self, event):
        cur_event = None
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            cur_event = SwitchScreenEvent(Conf.MENU)
            self.event_manager.post(cur_event, Conf.ALL)
        elif event.type == MOUSEBUTTONDOWN:
            button = event.button
            if button == 1:
                cur_event = MouseClickEvent(event.pos)
                self.event_manager.post(cur_event, Conf.VIEW)


class EndGameController(MVCObject):
    def __init__(self, ev_manager):
        MVCObject.__init__(self, ev_manager, '[contr_options_d]')

    def does_handle_event(self, event):
        if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN or event.type == MOUSEMOTION:
            return 1
        return 0

    def handle_py_game_event(self, event):
        cur_event = None
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            cur_event = SwitchScreenEvent(Conf.MENU)
            self.event_manager.post(cur_event, Conf.ALL)
        elif event.type == MOUSEBUTTONDOWN:
            button = event.button
            if button == 1:
                cur_event = MouseClickEvent(event.pos)
                self.event_manager.post(cur_event, Conf.VIEW)


class KeyboardController:
    """KeyboardController takes Pygame events generated by the
    keyboard and uses them to control the model, by sending Requests
    or to control the Pygame display directly, as with the QuitEvent
    """
    def __init__(self, ev_manager):
        self.event_manager = ev_manager
        self.event_manager.register_listener(self)

    def notify(self, event):
        if isinstance(event, TickEvent):
            # Handle Input Events
            for event in pygame.event.get():
                cur_event = None
                if event.type == QUIT:
                    cur_event = QuitEvent()
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    cur_event = QuitEvent()
                elif event.type == KEYDOWN and event.key == K_UP:
                    pass
                elif event.type == KEYDOWN and event.key == K_DOWN:
                    pass
                elif event.type == KEYDOWN and event.key == K_LEFT:
                    pass
                elif event.type == KEYDOWN and event.key == K_RIGHT:
                    pass
                if cur_event:
                    self.event_manager.post(cur_event)


class MouseController:
    """Mouse controller responsible for mouse events"""
    def __init__(self, ev_manager):
        self.event_manager = ev_manager
        self.event_manager.register_listener(self)

    def notify(self, event):
        if isinstance(event, TickEvent):
            # Handle Input Events
            for event in pygame.event.get():
                cur_event = None

                if event.type == QUIT:
                    cur_event = QuitEvent()
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    cur_event = QuitEvent()
                elif event.type == KEYDOWN and event.key == K_UP:
                    pass
                elif event.type == KEYDOWN and event.key == K_DOWN:
                    pass
                elif event.type == KEYDOWN and event.key == K_LEFT:
                    pass
                elif event.type == KEYDOWN and event.key == K_RIGHT:
                    pass
                if cur_event:
                    print("Keyboard Controller post: " + cur_event.name)
                    self.event_manager.post(cur_event)


if __name__ == "__main__":
    raise Exception("Unexpected")