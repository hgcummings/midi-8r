class Template:
    format = "B"

    def __init__(self, midi_out):
        self.midi_out = midi_out
        self.alert = False

    def load(self, data):
        self.state = data[0]
        self.saved_state = self.state

    def save(self):
        return (self.state,)

    def show_view(self, display):
        display.show_text(str(self.state))

    def clear_alert(self):
        self.alert = False

    def edit(self, display):
        self.__show_edit(display)
        return (0, self.state, 255)

    def update_value(self, value, display):
        self.state = value
        self.__show_edit(display)

    def switch(self, display):
        self.state = 255 - self.state
        self.__show_edit(display)

    def next(self):
        return None
    
    def __show_edit(self, display):
        display.show_text(str(self.state),
            colour=(32,255,32) if self.state == self.saved_state else (127,0,0))