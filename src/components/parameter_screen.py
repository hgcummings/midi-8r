from components import colours

class ParameterScreen:
    def __init__(self, param):
        self.format = param.format
        self.param = param

    @property
    def alert(self):
        return getattr(self.param, 'alert', False)

    def clear_alert(self):
        if hasattr(self.param, 'clear_alert'):
            self.param.clear_alert()

    def load(self, data):
        self.param.load(data)

    def save(self):
        return self.param.save()

    def show_view(self, display):
        self.param.render(display)

    def edit(self, display):
        while getattr(self.param, 'alert', False):
            self.param.clear_alert()
        self.__show_edit(display)
        return self.param.value_range()

    def update_value(self, value, display):
        self.param.update_value(value)
        self.__show_edit(display)

    def __show_edit(self, display):
        self.param.render(display, colours.MODIFIED if self.param.has_changed() else colours.SAVED)

    def switch(self, display):
        self.param.switch()
        self.__show_edit(display)

    def set_nav(self, nav):
        self._nav = nav

    def button_down(self, *_):
        pass

    def button_up(self, *_):
        if hasattr(self.param, 'advance') and self.param.advance():
            self._nav.refresh()
        else:
            self._nav.exit()
