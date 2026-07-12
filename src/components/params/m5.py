MIDI_CHANNEL = 1 # Zero-indexed, so this is MIDI Channel 2
MIDI_CC_ON_OFF = 11

MIN_PRESET = 1
MAX_PRESET = 24

class M5:
    """
    Parameter for selecting the preset on the Line 6 M5 pedal, which supports 24 patches

    Footswitch selects whether the M5 effect should be initially on or off whenever this patch is loaded
    """
    format = "b"
    alert = False

    def __init__(self, midi_out):
        self.midi_out = midi_out

    def load(self, data):
        if (data[0] == 0):
            # No patch saved; loaded empty data
            self.preset = 1
            self.init_on = False
        else:
            self.preset = abs(data[0])
            self.init_on = (self.preset == data[0]) # Init off stored as negative

        self.saved_preset = self.preset
        self.saved_init_on = self.init_on
        self.__update_midi()

    def value_range(self):
        return (MIN_PRESET, self.preset, MAX_PRESET)

    def update_value(self, value):
        self.preset = value
        self.__update_midi()

    def switch(self):
        self.init_on = not self.init_on
        self.__update_midi()

    def has_changed(self):
        return self.preset != self.saved_preset or self.init_on != self.saved_init_on

    def render(self, display, colour=None):
        display.show_text(
            "P{}".format(self.preset),
            line2_text="(on)" if self.init_on else "(off)",
            line2_indent=1,
            colour=colour)

    def save(self):
        self.saved_preset = self.preset
        self.saved_init_on = self.init_on
        return (self.preset * (1 if self.init_on else -1),)

    def __update_midi(self):
        self.midi_out.send_program_change(MIDI_CHANNEL, self.preset - 1)
        self.midi_out.send_control_change(MIDI_CHANNEL, MIDI_CC_ON_OFF, 127 if self.init_on else 0)
