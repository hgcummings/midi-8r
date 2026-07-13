from .parameter_screen import ParameterScreen

class PresetMenu:
    """
    Screen for navigating between the preset parameters

    Display order is determined by parameters flagging alerts,
    then by the order in which parameters were initially provided

    The rotary encoder is used to select a parameter to view or edit

    The footswitch is used to acknowledge (and clear) an alert
    from the parameter currently being displayed
    """
    def __init__(self, params):
        self.params = [ParameterScreen(param) for param in params]
        self.current_param = 0
        self.last_selected_param = 0

    def set_nav(self, nav):
        self._nav = nav

    def __render(self, display):
        self.params[self.current_param].render_view(display)

    def __update_current_param(self):
        self.current_param = self.last_selected_param
        for i, param in enumerate(self.params):
            if param.alert:
                self.current_param = i
                break

    def switch(self, display):
        if (self.params[self.current_param].alert):
            self.params[self.current_param].clear_alert()
            self.__update_current_param()
            self.__render(display)
        else:
            self.params[self.current_param].switch(display)

    def activate(self, display):
        self.__update_current_param()
        self.__render(display)
        return (0, self.current_param, len(self.params) - 1)

    def update_value(self, value, display):
        self.last_selected_param = value
        self.current_param = value
        self.params[self.current_param].render_view(display)

    def button_down(self, *_):
        pass

    def button_up(self, *_):
        self._nav.enter(self.params[self.current_param])
