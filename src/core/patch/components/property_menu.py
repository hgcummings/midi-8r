class PropertyMenu:
    """
    Menu component that supports navigation between multiple property components

    Display order is determined by components flagging alerts,
    then by the order in which components were initially provided

    The rotary encoder is used to select components to view or edit

    The footswitch is used to acknowledge (and clear) an alert
    from the component currently being displayed
    """
    def __init__(self, props):
        self.props = props
        self.current_prop = 0
        self.last_selected_prop = 0

    def __show_edit(self, display):
        self.current_prop = self.last_selected_prop
        for i, prop in enumerate(self.props):
            if prop.alert:
                self.current_prop = i
                break
        self.props[self.current_prop].show_view(display)

    def switch(self, display):
        if (self.props[self.current_prop].alert):
            self.props[self.current_prop].clear_alert()
            self.__show_edit(display)

    def edit(self, display):
        self.__show_edit(display)
        return (0, self.current_prop, len(self.props) - 1)

    def update_value(self, value, display):
        self.last_selected_prop = value
        self.current_prop = value
        self.props[self.current_prop].show_view(display)

    def next(self):
        return self.props[self.current_prop]
