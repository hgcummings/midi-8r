from components import colours
from components.params import load_empty

class DirectMenu:
    """
    Screen for editing parameters directly (rehearsal mode), without saving to a patch

    The rotary encoder edits the current parameter's value; push-and-turn switches
    between parameters
    """
    def __init__(self, params):
        self.params = params
        self.current_param = 0
        self.switching_params = False

        for param in params:
            load_empty(param)

    def set_nav(self, nav):
        self._nav = nav

    def activate(self, display):
        self.__render(display)
        if self.switching_params:
            return (0, self.current_param, len(self.params) - 1)
        else:
            return self.params[self.current_param].value_range()

    def update_value(self, value, display):
        if (self.switching_params):
            self.current_param = value
        else:
            self.params[self.current_param].update_value(value)
        self.__render(display)

    def __render(self, display):
        self.params[self.current_param].render(display, colours.REHEARSAL)

    def switch(self, display):
        self.params[self.current_param].switch()
        self.__render(display)

    def button_down(self, *_):
        self.switching_params = True
        self._nav.refresh()

    def button_up(self, *_):
        self.switching_params = False
        self._nav.refresh()
