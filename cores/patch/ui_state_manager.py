class UiStateManager:
    def __init__(self, initial_component, control, display):
        # External state-holding objects
        self._control = control
        self._display = display

        # Internal state
        self.set_component(initial_component)

    def set_component(self, component):
        self._component = component
        self._control.set_range_and_value(*self._component.edit(self._display))

    def edit(self):
        return self._component.edit(self._display)

    def update_value(self, value):
        self._component.update_value(value, self._display)

    def switch(self):
        self._component.switch(self._display)

    def next(self):
        return self._component.next()