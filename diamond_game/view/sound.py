import sys
import time
from diamond_game import *


class SoundView(MVCObject):
    def __init__(self, ev_manager):
        MVCObject.__init__(self, ev_manager, '[sound_view]')
        self.sounds = {}

    @property
    def get_next_event(self):
        return self.event_manager.get_next_sound_event()

    # noinspection PyBroadException
    def run(self):
        self.sounds = Utils.load_all_sounds()
        running = 1
        try:
            while running:
                # Check sounds's event queue
                event = self.get_next_event
                # Handle events
                # If quit event then terminate
                if isinstance(event, QuitEvent):
                    print self.thread_name + ' is shutting down'
                    # play all sounds before shutting down
                    time.sleep(0.5)
                    running = 0
                elif isinstance(event, SoundPlayEvent):
                    self.sounds[event.sound_name].play()
        except:
            e = sys.exc_info()[0]
            print '>>>>>>>>>>> Fatal Error in: ' + self.thread_name
            print e
            self.post(QuitEvent(), Conf.ALL)