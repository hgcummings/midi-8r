class Navigator:
    """
    Owns all mutable state.

    Tracks a current screen and an optional previous one, routing input events to the
    current screen. Screens navigate by calling enter, exit, and refresh on the
    navigator they receive via set_nav when activated.
    """
    def __init__(self, initial_screen, control, display, on_save):
        self._control = control
        self._display = display
        self._on_save = on_save
        self._current = None
        self._previous = None

        control.observe_value(self.__on_value)
        control.observe_footswitch(self.__on_switch)
        control.observe_button_down(self.__on_button_down)
        control.observe_button_up(self.__on_button_up)

        self.set_screen(initial_screen)

    @property
    def _current(self):
        return self.__current

    @_current.setter
    def _current(self, screen):
        self.__current = screen
        if screen is not None:
            screen.set_nav(self)

    def set_screen(self, screen):
        """Replace the current screen. Called by PatchEditor on program change."""
        self._previous = None
        self._current = screen
        self.__activate(screen)

    def enter(self, screen):
        self._previous = self._current
        self._current = screen
        self.__activate(screen)

    def exit(self):
        self._current = self._previous
        self._previous = None
        self.__activate(self._current)
        self._on_save()

    def refresh(self):
        self.__activate(self._current)

    def __activate(self, screen):
        self._control.set_range_and_value(*screen.activate(self._display))

    def __on_value(self, value):
        self._current.update_value(value, self._display)

    def __on_switch(self):
        self._current.switch(self._display)

    def __on_button_down(self):
        self._current.button_down(self._display)

    def __on_button_up(self):
        self._current.button_up(self._display)
