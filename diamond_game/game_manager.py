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
        Event.__init__(self, "Switch Screen Event: " + Conf.debug_dict.get(val))
        self.value = val


class BoardCreatedEvent(Event):
    def __init__(self, val, dimention):
        Event.__init__(self, "Board Create Event: " + str(val) + " " + str(dimention))
        self.value = val
        self.dimention = dimention


class PiecesCreatedEvent(Event):
    def __init__(self, val):
        Event.__init__(self, "Pieces Create Event: " + str(val))
        self.value = val


class SubModulesLoadedEvent(Event):
    def __init__(self, module, sub_module):
        Event.__init__(self, "SubModulesLoadedEvent: " +
                       Conf.debug_dict.get(module) + ": " +
                       Conf.debug_dict.get(sub_module))
        self.module = module
        self.sub_module = sub_module


class GameObjectClickEvent(Event):
    def __init__(self, typ, val):
        Event.__init__(self, "GameObjectClickEvent: " + str(typ) + " " + str(val))
        self.typ = typ
        self.value = val


class HintsCreatedEvent(Event):
    def __init__(self, val):
        Event.__init__(self, "HintsCreatedEvent: " + str(val))
        self.value = val


class HintsDestroyedEvent(Event):
    def __init__(self):
        Event.__init__(self, "HintsDestroyedEvent")


class PieceSelectedEvent(Event):
    """Has uid piece attribute
    """
    def __init__(self, uid):
        Event.__init__(self, "PieceSelectedEvent: " + str(uid))
        self.value = uid


class PieceDeSelectedEvent(Event):
    """Has uid piece attribute
    """
    def __init__(self, uid):
        Event.__init__(self, "PieceDeSelectedEvent: " + str(uid))
        self.value = uid


class PieceMoveEvent(Event):
    def __init__(self, start, end):
        Event.__init__(self, "PieceMoveEvent: " + str(start) + " " + str(end))
        self.start = start
        self.end = end


class CreateAvailableLocs(Event):
    def __init__(self, locs):
        Event.__init__(self, "CreateAvailableLocs: " + str(locs))
        self.locs = locs


class RemoveAvailableLocs(Event):
    def __init__(self, locs):
        Event.__init__(self, "RemoveAvailableLocs: " + str(locs))
        self.locs = locs


class SoundPlayEvent(Event):
    def __init__(self, sound_name):
        Event.__init__(self, "SoundPlayEvent: " + str(sound_name))
        self.sound_name = sound_name


class EventManager(object):
    """Class to manage all of the events generated in the Game"""
    def __init__(self):
        # A dict in which items get deleted if either
        # the key or the value of the item is garbage collected.
        self.model_event_queue = Queue.Queue(0)
        self.view_event_queue = Queue.Queue(0)
        self.controller_event_queue = Queue.Queue(0)
        self.sound_event_queue = Queue.Queue(0)
        # locks to queue access
        self.model_locked = 0
        self.view_locked = 0
        self.controller_locked = 0

    def post(self, event, destination):
        """
        Method that allows to
        pass events to corresponding parts of the program
        events are not posted if the resource is locked
        """
        if destination == Conf.ALL:
            # Only switch and quit events are send to all
            self.view_event_queue.put(event)
            self.model_event_queue.put(event)
            self.controller_event_queue.put(event)
            self.sound_event_queue.put(event)
        elif destination == Conf.MODEL:
            if not self.model_locked:
                self.model_event_queue.put(event)
        elif destination == Conf.VIEW:
            if not self.view_locked:
                self.view_event_queue.put(event)
        elif destination == Conf.CONTROLLER:
            if not self.controller_locked:
                self.controller_event_queue.put(event)
        elif destination == Conf.SOUND:
                self.sound_event_queue.put(event)
        if Conf.DEBUG:
            self.debug(event, destination)

    def manage_lock(self, thread_to_lock, action):
        """
        Method that allows to optionally allow or
        disallow adding events to queues.
        If queue is locked for access then events will miss out
        """
        if thread_to_lock == Conf.MODEL:
            self.model_locked = action
        elif thread_to_lock == Conf.VIEW:
            self.view_locked = action
        elif thread_to_lock == Conf.CONTROLLER:
            self.controller_locked = action

    def get_next_model_event(self):
        """
        :return:
        :rtype : Event
        """
        if not self.model_event_queue.empty():
            return self.model_event_queue.get()

    def get_next_view_event(self):
        """
        :return:
        :rtype : Event
        """
        if not self.view_event_queue.empty():
            return self.view_event_queue.get()

    def get_next_controller_event(self):
        """
        :return:
        :rtype : Event
        """
        if not self.controller_event_queue.empty():
            return self.controller_event_queue.get()

    def get_next_sound_event(self):
        """
        :return:
        :rtype : Event
        """
        if not self.sound_event_queue.empty():
            return self.sound_event_queue.get()

    @staticmethod
    def debug(event, destination):
        if not isinstance(event, TickEvent):
            print '[' + event.name + '] send to [' + Conf.debug_dict.get(destination) + ']'


class MVCObject(Thread):
    def __init__(self, ev_manager, name):
        Thread.__init__(self)
        self.thread_name = name
        self.id = 0
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
        self.post(SubModulesLoadedEvent(self.id, key), Conf.ALL)

if __name__ == "__main__":
    raise Exception("Unexpected")
