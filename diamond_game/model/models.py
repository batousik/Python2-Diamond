from diamond_game import *


class MasterModel(MVCObject):
    def __init__(self, ev_manager):
        MVCObject.__init__(self, ev_manager)
        self.model_classes = {'menu': [MenuModel]}
        self.sub_models = []
        self.switch_model('menu')

    def notify(self, event):
        # Handle events
        for model in self.sub_models:
            # Look for a model that accepts event
            if model.does_handle_event(event):
                # Let model handle event
                model.handle_event(event)
                # Stop other models from handling current event
                break
        # Change screen request
        # elif isinstance(event, 1):
        #     self.switch_controller(event.key)

        # elif isinstance( incomingEvent, GUIDialogAddRequest ):
        # self.DialogAdd( incomingEvent.key )
        #
        # elif isinstance( incomingEvent, GUIDialogRemoveRequest ):
        # self.DialogRemove( incomingEvent.key )

    def switch_model(self, key):
        if not self.model_classes.has_key(key):
            raise NotImplementedError
        self.sub_models = []
        for model_class in self.model_classes[key]:
            new_model = model_class(self.event_manager)
            self.sub_models.append(new_model)


class MenuModel(MVCObject):
    def __init__(self, ev_manager):
        MVCObject.__init__(self, ev_manager)
        self.data = ['Start Game', 'Options', 'Exit']
        self.chosen = 0

    def does_handle_event(self, event):
        if isinstance(event, TickEvent):
            return 0
        return 1

    def handle_event(self, event):
        if isinstance(event, MenuPrevEvent):
            self.post(MenuUnSelectEvent(self.chosen))
            if self.chosen == 0:
                self.chosen = len(self.data) - 1
            else:
                self.chosen -= 1
            self.post(MenuSelectEvent(self.chosen))
        elif isinstance(event, MenuNextEvent):
            self.post(MenuUnSelectEvent(self.chosen))
            if self.chosen < len(self.data)-1:
                self.chosen += 1
            else:
                self.chosen = 0
            self.post(MenuSelectEvent(self.chosen))
        elif isinstance(event, MenuPressEvent):
            print("Model would choose: " + self.data[self.chosen])
