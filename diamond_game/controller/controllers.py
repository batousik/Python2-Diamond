import pygame
from pygame.constants import *
from diamond_game import *
import random


class MasterController(MVCObject):
    def __init__(self, ev_manager):
        MVCObject.__init__(self, ev_manager)
        # sub controllers is an ordered list,
        # the first controller in the
        # list is the first to be offered an event
        self.sub_controllers = []
        self.controller_classes = {'menu': [MenuController], 'game': [GameController], 'options': [OptionsController]}
        self.sub_controllers = {'msgDialog': 1}
        self.switch_controller('menu')

    def notify(self, event):
        # If next tick occurred, go through
        # PyGame events queue and handle them
        if isinstance(event, TickEvent):
            # Handle All PyGame Events
            for py_game_event in pygame.event.get():
                # Game end event
                if py_game_event.type == QUIT:
                    cur_event = QuitEvent()
                    self.event_manager.post(cur_event)
                else:
                    # Go through all controllers
                    for controller in self.sub_controllers:
                        # Look for a controller that accepts event
                        if controller.does_handle_event(py_game_event):
                            # Let controller handle event
                            controller.handle_py_game_event(py_game_event)
                            # Stop other controllers from handling current event
                            break
        # Change screen request
        elif isinstance(event, SwitchScreenEvent):
            self.switch_controller(event.value)

    def switch_controller(self, key):
        if not self.controller_classes.has_key(key):
            raise NotImplementedError
        self.sub_controllers = []
        for controller_class in self.controller_classes[key]:
            new_controller = controller_class(self.event_manager)
            self.sub_controllers.append(new_controller)


class MenuController(MVCObject):
    def __init__(self, ev_manager):
        MVCObject.__init__(self, ev_manager)

    def does_handle_event(self, event):
        if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN or event.type == MOUSEMOTION:
            return 1
        return 0

    def handle_py_game_event(self, event):
        cur_event = None
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            cur_event = QuitEvent()
        elif event.type == KEYDOWN and event.key == K_UP:
            cur_event = MenuPrevEvent()
        elif event.type == KEYDOWN and event.key == K_DOWN:
            cur_event = MenuNextEvent()
        elif event.type == KEYDOWN and (event.key == K_RETURN or event.key == K_SPACE):
            cur_event = MenuPressEvent()
        elif event.type == MOUSEBUTTONDOWN:
            button = event.button
            if button == 1:
                cur_event = MouseClickEvent(event.pos)
        elif event.type == MOUSEMOTION:
            cur_event = MouseMotionEvent(event.pos)
        if cur_event:
            self.event_manager.post(cur_event)


class GameController(MVCObject):
    def __init__(self, ev_manager):
        MVCObject.__init__(self, ev_manager)

    def does_handle_event(self, event):
        if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN or event.type == MOUSEMOTION:
            return 1
        return 0

    def handle_py_game_event(self, event):
        cur_event = None
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            cur_event = QuitEvent()
        elif event.type == KEYDOWN and event.key == K_UP:
            cur_event = MenuPrevEvent()
        elif event.type == KEYDOWN and event.key == K_DOWN:
            cur_event = MenuNextEvent()
        elif event.type == KEYDOWN and (event.key == K_RETURN or event.key == K_SPACE):
            cur_event = MenuPressEvent()
        elif event.type == MOUSEBUTTONDOWN:
            button = event.button
            if button == 1:
                cur_event = MouseClickEvent(event.pos)
        elif event.type == MOUSEMOTION:
            cur_event = MouseMotionEvent(event.pos)
        if cur_event:
            self.event_manager.post(cur_event)


class OptionsController(MVCObject):
    def __init__(self, ev_manager):
        MVCObject.__init__(self, ev_manager)

    def does_handle_event(self, event):
        if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN or event.type == MOUSEMOTION:
            return 1
        return 0

    def handle_py_game_event(self, event):
        cur_event = None
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            cur_event = QuitEvent()
        elif event.type == KEYDOWN and event.key == K_UP:
            cur_event = MenuPrevEvent()
        elif event.type == KEYDOWN and event.key == K_DOWN:
            cur_event = MenuNextEvent()
        elif event.type == KEYDOWN and (event.key == K_RETURN or event.key == K_SPACE):
            cur_event = MenuPressEvent()
        elif event.type == MOUSEBUTTONDOWN:
            button = event.button
            if button == 1:
                cur_event = MouseClickEvent(event.pos)
        elif event.type == MOUSEMOTION:
            cur_event = MouseMotionEvent(event.pos)
        if cur_event:
            self.event_manager.post(cur_event)



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


class SpinnerController(MVCObject):
    """Class that has while loop to issue game tick events"""
    def __init__(self, ev_manager):
        super(SpinnerController, self).__init__(ev_manager)
        self.running = True
        self.event_manager = ev_manager
        self.event_manager.register_listener(self)

    def run(self):
        while self.running:
            event = TickEvent()
            self.event_manager.post(event)

    def notify(self, event):
        if isinstance(event, QuitEvent):
            # Quits the game
            self.running = False

if __name__ == "__main__":
    raise Exception("Unexpected")