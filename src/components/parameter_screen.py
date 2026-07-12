from components import colours

class ParameterScreen:
    def __init__(self, prop):
        self.format = prop.format
        self.prop = prop

    @property
    def alert(self):
        return getattr(self.prop, 'alert', False)

    def clear_alert(self):
        if hasattr(self.prop, 'clear_alert'):
            self.prop.clear_alert()

    def load(self, data):
        self.prop.load(data)

    def save(self):
        return self.prop.save()

    def show_view(self, display):
        self.prop.render(display)

    def edit(self, display):
        while getattr(self.prop, 'alert', False):
            self.prop.clear_alert()
        self.__show_edit(display)
        return self.prop.value_range()

    def update_value(self, value, display):
        self.prop.update_value(value)
        self.__show_edit(display)

    def __show_edit(self, display):
        self.prop.render(display, colours.MODIFIED if self.prop.has_changed() else colours.SAVED)

    def switch(self, display):
        self.prop.switch()
        self.__show_edit(display)

    def set_nav(self, nav):
        self._nav = nav

    def button_down(self, *_):
        pass

    def button_up(self, *_):
        if hasattr(self.prop, 'advance') and self.prop.advance():
            self._nav.refresh()
        else:
            self._nav.exit()
