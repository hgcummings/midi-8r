class PresetMenu:
    """
    Menu component that supports navigation between multiple preset components

    Display order is determined by components flagging alerts,
    then by the order in which components were initially provided

    The rotary encoder is used to select components to view or edit

    The footswitch is used to acknowledge (and clear) an alert
    from the component currently being displayed
    """
    def __init__(self, params):
        self.params = params
        self.current_param = 0
        self.last_selected_prop = 0

    def set_nav(self, nav):
        self._nav = nav

    def __show_edit(self, display):
        self.current_param = self.last_selected_prop
        for i, param in enumerate(self.params):
            if param.alert:
                self.current_param = i
                break
        self.params[self.current_param].show_view(display)

    def switch(self, display):
        if (self.params[self.current_param].alert):
            self.params[self.current_param].clear_alert()
            self.__show_edit(display)
        self.params[self.current_param].switch(display)

    def edit(self, display):
        self.__show_edit(display)
        return (0, self.current_param, len(self.params) - 1)

    def update_value(self, value, display):
        self.last_selected_prop = value
        self.current_param = value
        self.params[self.current_param].show_view(display)

    def button_down(self, *_):
        pass

    def button_up(self, *_):
        self._nav.enter(self.params[self.current_param])
