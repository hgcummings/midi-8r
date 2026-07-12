from components import colours

MIDI_CHANNEL = 0
MIDI_CC_NRPN_LSB = 98
MIDI_CC_NRPN_MSB = 99
MIDI_CC_DATA_LSB = 38
MIDI_CC_DATA_MSB = 6

class Tempo:
    """
    Parameter for setting the tempo on the Nux Cerberus

    Does _not_ automatically set the tempo on load but sets it on pressing the footswitch.
    To set the tempo on load, save it to the Cerberus preset.
    """
    format = "H"

    def __init__(self, midi_out):
        self.midi_out = midi_out

    def load(self, data):
        self.applied = False
        if (data[0] == 0):
            # No patch saved; loaded empty data
            self.bpm = 120
        else:
            self.bpm = data[0]
        self.saved_bpm = self.bpm

    def value_range(self):
        return (40, self.bpm, 480)

    def update_value(self, value):
        self.bpm = value
        self.__update_midi()

    def switch(self):
        self.__update_midi()

    def has_changed(self):
        return self.bpm != self.saved_bpm

    def render(self, display, colour=None):
        if colour is None:
            colour = colours.VIEW if self.applied else colours.PENDING
        display.show_text(
            str(self.bpm),
            line2_text="BPM",
            colour=colour,
            line2_indent=5)

    def save(self):
        self.saved_bpm = self.bpm
        return (self.bpm,)

    def __update_midi(self):
        self.applied = True
        value14 = round((self.bpm - 40) / 440 * 16383)
        self.midi_out.send_control_change(MIDI_CHANNEL, MIDI_CC_NRPN_LSB, 6)
        self.midi_out.send_control_change(MIDI_CHANNEL, MIDI_CC_NRPN_MSB, 38)
        self.midi_out.send_control_change(MIDI_CHANNEL, MIDI_CC_DATA_MSB, value14 >> 7)
        self.midi_out.send_control_change(MIDI_CHANNEL, MIDI_CC_DATA_LSB, value14 & 0x7f)
