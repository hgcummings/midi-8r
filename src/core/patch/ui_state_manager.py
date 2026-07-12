class UiStateManager:
    """
    All updates to mutable UI state are the responsibility of this class.

    This class delegates responsibility for updating the display to other components,
    but only ever to one component at a time, and only in response to specific events.
    """
    def __init__(self, initial_component, control, display):
        # External state-holding objects
        self._control = control
        self._display = display

        # Internal state
        self.set_component(initial_component)

    def set_component(self, component) -> None:
        """Set the current component and update UI state accordingly"""
        self._component = component
        self._control.set_range_and_value(*self._component.edit(self._display))
        self._component.observe_next(self.set_component)

    def update_value(self, value) -> None:
        """Inform the current component of an update to the selected value"""
        self._component.update_value(value, self._display)

    def switch(self) -> None:
        """"Inform the current component of the switch being pressed"""
        self._component.switch(self._display)

    def button_down(self) -> None:
        self._component.button_down(self._display)

    def button_up(self) -> None:
        self._component.button_up(self._display)