class Event(object):
    """Generic event class, all Events should extend this class"""
    def __init__(self):
        self.name = "Generic Event"


class TickEvent(Event):
    def __init__(self):
        self.name = "Tick Event"


class QuitEvent(Event):
    def __init__(self):
        self.name = "Quit Event"


class MenuPrevEvent(Event):
    def __init__(self):
        self.name = "Select Previous Menu Entry Event"


class MenuNextEvent(Event):
    def __init__(self):
        self.name = "Select Next Menu Entry Event"


class MenuPressEvent(Event):
    def __init__(self):
        self.name = "Execute menu entry Event"


class MenuClickEvent(Event):
    def __init__(self, pos):
        self.name = "Menu mouse clicked event: " + str(pos)
        self.position = pos


class MenuMouseMotionEvent(Event):
    def __init__(self, pos):
        self.name = "Menu mouse moved event: " + str(pos)
        self.position = pos


class EventManager:
    """Class to manage all of the events generated in the Game"""
    def __init__(self):
        # A dict in which items get deleted if either
        # the key or the value of the item is garbage collected.
        from weakref import WeakKeyDictionary
        self.listeners = WeakKeyDictionary()

    def register_listener(self, listener):
        self.listeners[listener] = 1

    def un_register_listener(self, listener):
        if listener in self.listeners.keys():
            del self.listeners[listener]

    def debug(self, event):
        if not isinstance(event, TickEvent):
            print event.name

    def post(self, event):
        self.debug(event)
        """Post a new event.  It will be broadcast to all listeners"""
        for listener in self.listeners.keys():
            listener.notify(event)