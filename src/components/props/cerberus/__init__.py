class PresetEditor:
    def __init__(self, prop):
        self.format = prop.format
        self.prop = prop
        self.alert = False

    def load(self, data):
        self.prop.load(data)

    def save(self):
        return self.prop.save()

    def show_view(self, display):
        self.prop.show_text(display)

    def edit(self, display):
        self.__show_edit(display)
        return self.prop.value_range()

    def update_value(self, value, display):
        self.prop.update_value(value)
        self.__show_edit(display)

    def __show_edit(self, display):
        self.prop.show_text(display, (127,0,0) if self.prop.has_changed() else (32,255,32))

    def switch(self, display):
        self.prop.switch()
        self.__show_edit(display)

    def observe_next(self, next_observer):
        self._next_observer = next_observer

    def button_down(self, *_):
        pass

    def button_up(self, *_):
        self._next_observer(self.parent)
        self.parent.on_save()
