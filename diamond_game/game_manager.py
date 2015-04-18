import Queue
from threading import Thread
from diamond_game import Conf


class Event(object):
    """Generic event class, all Events should extend this class"""
    def __init__(self, name):
        self.name = name


class TickEvent(Event):
    def __init__(self):
        Event.__init__(self, "Tick Event")


class QuitEvent(Event):
    def __init__(self):
        Event.__init__(self, "Quit Event")


class MenuPrevEvent(Event):
    def __init__(self):
        Event.__init__(self, "Select Previous Menu Entry Event")


class MenuNextEvent(Event):
    def __init__(self):
        Event.__init__(self, "Select Next Menu Entry Event")


class MenuPressEvent(Event):
    def __init__(self):
        Event.__init__(self, "Menu Press Event")


class MouseClickEvent(Event):
    def __init__(self, pos):
        Event.__init__(self, "Mouse Clicked Event: " + str(pos))
        self.position = pos


class MouseMotionEvent(Event):
    def __init__(self, pos):
        Event.__init__(self, "Mouse Moved Event: " + str(pos))
        self.position = pos


class MenuSelectEvent(Event):
    def __init__(self, val):
        Event.__init__(self, "Menu Select Event: " + str(val))
        self.value = val


class MenuUnSelectEvent(Event):
    def __init__(self, val):
        Event.__init__(self, "Menu Un Select Event: " + str(val))
        self.value = val


class ButtonHoverEvent(Event):
    def __init__(self, val):
        Event.__init__(self, "Hover Event: " + str(val))
        self.value = val


class SwitchScreenEvent(Event):
    def __init__(self, val):
        Event.__init__(self, "Switch Screen Event: " + str(val))
        self.value = val


class BoardCreatedEvent(Event):
    def __init__(self, val):
        Event.__init__(self, "Board Create Event: " + str(val))
        self.value = val


class PiecesCreatedEvent(Event):
    def __init__(self, val):
        Event.__init__(self, "Pieces Create Event: " + str(val))
        self.value = val


class EventManager(object):
    """Class to manage all of the events generated in the Game"""
    def __init__(self):
        # A dict in which items get deleted if either
        # the key or the value of the item is garbage collected.
        self.model_event_queue = Queue.Queue(0)
        self.view_event_queue = Queue.Queue(0)
        self.controller_event_queue = Queue.Queue(0)

    def post(self, event, destination):
        """
        Method that allows to
        pass events to corresponding parts of the program
        """
        if destination == Conf.ALL:
            self.view_event_queue.put(event)
            self.model_event_queue.put(event)
            self.controller_event_queue.put(event)
        elif destination == Conf.MODEL:
            self.model_event_queue.put(event)
        elif destination == Conf.VIEW:
            self.view_event_queue.put(event)
        elif destination == Conf.CONTROLLER:
            self.controller_event_queue.put(event)
        self.debug(event, destination)
        """Post a new event.  It will be broadcast to all listeners"""

    def get_next_model_event(self):
        """
        :rtype : Event
        """
        if not self.model_event_queue.empty():
            return self.model_event_queue.get()

    def get_next_view_event(self):
        """
        :rtype : Event
        """
        if not self.view_event_queue.empty():
            return self.view_event_queue.get()

    def get_next_controller_event(self):
        """
        :rtype : Event
        """
        if not self.controller_event_queue.empty():
            return self.controller_event_queue.get()

    @staticmethod
    def debug(event, destination):
        if not isinstance(event, TickEvent):
            print '[' + event.name + '] send to [' + Conf.debug_dict.get(destination) + ']'


class MVCObject(Thread):
    def __init__(self, ev_manager, name):
        Thread.__init__(self)
        self.thread_name = name
        self.event_manager = ev_manager
        self.sub_modules = []
        self.sub_classes = {}

    def does_handle_event(self, event):
        print 'In ' + self.thread_name + ' does_handle_event method is not implemented'

    def handle_event(self, event):
        print 'In ' + self.thread_name + ' handle_event method is not implemented'

    def handle_py_game_event(self, event):
        print 'In ' + self.thread_name + ' handle_py_game_event method is not implemented'

    def post(self, event, destination):
        self.event_manager.post(event, destination)

    def run(self):
        print 'In ' + self.thread_name + ' run method is not implemented'

    def switch_sub_modules(self, key):
        if not self.sub_classes.has_key(key):
            raise NotImplementedError
        self.sub_modules = []
        for a_class in self.sub_classes[key]:
            new_module = a_class(self.event_manager)
            self.sub_modules.append(new_module)

if __name__ == "__main__":
    raise Exception("Unexpected")
