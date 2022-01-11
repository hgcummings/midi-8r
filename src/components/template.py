class Component:
    """
    Define the byte structure for storing this component's data.
    
    See https://docs.python.org/3/library/struct.html
    """
    format = "B"

    def __init__(self, midi_out):
        self.midi_out = midi_out
        self.alert = False

    def load(self, data):
        """
        `data` will be a tuple, loaded according to the defined `Component.format`.

        The component may use `midi_out` here to update other pedals with the loaded settings.

        The component may flag an alert here, for example if settings differ from the previously-
        loaded patch that can't be updated automatically, but require user intervention.
        """
        self.state = data[0]
        self.saved_state = self.state

    def save(self):
        """
        Return a tuple containing this component's data in the defined `Component.format`.
        """
        return (self.state,)

    def show_view(self, display):
        """
        Display this component's state in view mode
        """
        display.show_text(str(self.state))

    def clear_alert(self):
        """
        Clear a previously flagged alert, in response to the user acknowledging it.
        """
        self.alert = False

    def edit(self, display):
        """
        Display this component's state in edit mode.
        Return a tuple of the (min, current, max) values available for the user to select.
        """
        self.__show_edit(display)
        return (0, self.state, 255)

    def update_value(self, value, display):
        """
        Update the selected value and refresh the display.

        The component may use `midi_out` here to update other pedals with the selected settings.
        """
        self.state = value
        self.__show_edit(display)

    def switch(self, display):
        """
        (Optionally) respond to the footswitch and update the display.
        """
        self.state = 255 - self.state
        self.__show_edit(display)

    def next(self):
        """
        Nominate the next component after the user has finished editing the current value.

        Components should return themselves if they have more values to edit.
        (In this case, the `edit` method will be invoked again after this method)

        Components should return `None` if they do not need to choose the next component.
        """
        return None
    
    def __show_edit(self, display):
        display.show_text(str(self.state),
            colour=(32,255,32) if self.state == self.saved_state else (127,0,0))