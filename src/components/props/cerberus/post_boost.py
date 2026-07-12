MIDI_CHANNEL = 0
MIDI_CC_LEVEL = 103
MIDI_CC_ON_OFF = 104

class PostBoost:
    """
    Simple prop editor for setting the post-volume boost on the NUX Cerberus pedal
    Not a full component in itself. Needs to be wrapped in PresetEditor or DirectMenu
    """
    format = "b"

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

    def value_range(self):
        return (0, self.level, 127)

    def update_value(self, value):
        self.level = value
        self.__update_midi()

    def switch(self):
        self.on = not self.on
        self.__update_midi()

    def save(self):
        self.saved_level = self.level
        self.saved_on = self.on
        return (self.level * (1 if self.on else -1),)

    def has_changed(self):
        return self.level != self.saved_level or self.on != self.saved_on

    def render(self, display, colour=(255,255,255)):
        display.show_text(
            "{0:.1f}dB".format(6 * self.level / 127),
            line2_text="(on)" if self.on else "(off)",
            line2_indent=1,
            colour=colour)

    def __update_midi(self):
        self.midi_out.send_control_change(MIDI_CHANNEL, MIDI_CC_LEVEL, self.level)
        self.midi_out.send_control_change(MIDI_CHANNEL, MIDI_CC_ON_OFF, 127 if self.on else 0)
