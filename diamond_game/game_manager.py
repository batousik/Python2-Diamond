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
        from weakref import WeakKeyDictionary
        self.listeners = WeakKeyDictionary()

    def register_listener(self, listener):
        self.listeners[listener] = 1

    def un_register_listener(self, listener):
        if listener in self.listeners.keys():
            del self.listeners[listener]

    @staticmethod
    def debug(event):
        if not isinstance(event, TickEvent):
            print event.name

    def post(self, event):
        self.debug(event)
        """Post a new event.  It will be broadcast to all listeners"""
        for listener in self.listeners.keys():
            listener.notify(event)


class MVCObject(object):
    def __init__(self, ev_manager):
        self.event_manager = ev_manager
        self.event_manager.register_listener(self)

    def notify(self, event):
        pass

    def does_handle_event(self, event):
        pass

    def handle_event(self, event):
        pass

    def handle_py_game_event(self, event):
        pass

    def post(self, event):
        self.event_manager.post(event)


if __name__ == "__main__":
    raise Exception("Unexpected")
