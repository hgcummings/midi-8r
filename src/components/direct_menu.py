from components import colours

class DirectMenu:
    def __init__(self, props):
        self.props = props
        self.current_prop = 0
        self.switching_props = False

        for prop in props:
            prop.load([0])

    def set_nav(self, nav):
        self._nav = nav

    def edit(self, display):
        self.__show_edit(display)
        if self.switching_props:
            return (0, self.current_prop, len(self.props) - 1)
        else:
            return self.props[self.current_prop].value_range()

    def update_value(self, value, display):
        if (self.switching_props):
            self.current_prop = value
        else:
            self.props[self.current_prop].update_value(value)
        self.__show_edit(display)

    def __show_edit(self, display):
        self.props[self.current_prop].render(display, colours.REHEARSAL)

    def switch(self, display):
        self.props[self.current_prop].switch()
        self.__show_edit(display)

    def button_down(self, *_):
        self.switching_props = True
        self._nav.refresh()

    def button_up(self, *_):
        self.switching_props = False
        self._nav.refresh()
