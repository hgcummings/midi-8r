class Navigator:
    """
    Owns all mutable state.

    Tracks a current component and an optional previous one, routing input events to the
    current component. Components navigate by calling enter, exit, and refresh on the
    navigator they receive via set_nav when activated.
    """
    def __init__(self, initial_component, control, display, on_save):
        self._control = control
        self._display = display
        self._on_save = on_save
        self._current = None
        self._previous = None

        control.observe_value(self._on_value)
        control.observe_footswitch(self._on_switch)
        control.observe_button_down(self._on_button_down)
        control.observe_button_up(self._on_button_up)

        self.set_component(initial_component)

    def set_component(self, component):
        """Replace the current component. Called by PatchEditor on program change."""
        self._previous = None
        self._current = component
        self._activate(component)

    def enter(self, component):
        self._previous = self._current
        self._current = component
        self._activate(component)

    def exit(self):
        self._current = self._previous
        self._previous = None
        self._activate(self._current)
        self._on_save()

    def refresh(self):
        self._activate(self._current)

    def _activate(self, component):
        self._control.set_range_and_value(*component.edit(self._display))
        component.set_nav(self)

    def _on_value(self, value):
        self._current.update_value(value, self._display)

    def _on_switch(self):
        self._current.switch(self._display)

    def _on_button_down(self):
        self._current.button_down(self._display)

    def _on_button_up(self):
        self._current.button_up(self._display)
