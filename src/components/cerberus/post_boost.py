MIDI_CHANNEL = 0
MIDI_CC_LEVEL = 103
MIDI_CC_ON_OFF = 104

class PostBoost:
    """
    Component for setting the post-volume boost on the NUX Cerberus pedal
    """
    format = "b"
    alert = False

    def __init__(self, midi_out):
        self.midi_out = midi_out

    def load(self, data):
        if (data[0] == 0):
            # No patch saved; loaded empty data
            self.level = 0
            self.on = False
        else:
            self.level = abs(data[0])
            self.on = (self.level == data[0]) # Init off stored as negative

        self.saved_level = self.level
        self.saved_on = self.on

        self.__update_midi()

    def show_view(self, display):
        self.__show_current(display)

    def edit(self, display):
        self.__show_edit(display)
        return (0, self.level, 127)

    def update_value(self, value, display):
        self.level = value
        self.__show_edit(display)
        self.__update_midi()

    def switch(self, display):
        self.on = not self.on
        self.__update_midi()
        self.__show_edit(display)

    def next(self):
        return None

    def save(self):
        self.saved_level = self.level
        self.saved_on = self.on
        return (self.level * (1 if self.on else -1),)

    def __show_edit(self, display):
        self.__show_current(display,
            colour=(32,255,32) if self.level == self.saved_level and self.on == self.saved_on else (127,0,0))

    def __show_current(self, display, colour=(255,255,255)):
        display.show_text(
            "{0:.1f}dB".format(6 * self.level / 127),
            line2_text="(on)" if self.on else "(off)",
            line2_indent=1,
            colour=colour)

    def __update_midi(self):
        self.midi_out.send_control_change(MIDI_CHANNEL, MIDI_CC_LEVEL, self.level)
        self.midi_out.send_control_change(MIDI_CHANNEL, MIDI_CC_ON_OFF, 127 if self.on else 0)
