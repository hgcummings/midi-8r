MIDI_CHANNEL = 0
MIDI_CC_NRPN_LSB = 98
MIDI_CC_NRPN_MSB = 99
MIDI_CC_DATA_LSB = 38
MIDI_CC_DATA_MSB = 6

MODELS = ["J120","D112","B410","A212","T212","1960","G412","V412"]

class Tempo:
    """
    Component for setting the tempo on the Nux Cerberus
    Does _not_ automatically set the tempo on load but sets it on pressing the footswitch
    To set the tempo on load, save it to the Cerberus preset
    """
    format = "H"

    def __init__(self, midi_out):
        self.midi_out = midi_out
        self.alert = False

    def load(self, data):
        self.applied = False
        self.in_edit = False
        if (data[0] == 0):
            # No patch saved; loaded empty data
            self.bpm = 120
        else:
            self.bpm = data[0]

        self.saved_bpm = self.bpm

    def save(self):
        self.in_edit = False
        self.saved_bpm = self.bpm
        return (self.bpm,)

    def show_view(self, display):
        self.__show_current(display, colour=((255,255,255) if self.applied else (64,64,64)))

    def edit(self, display):
        self.in_edit = True
        self.__show_edit(display)
        return (40, self.bpm, 480)

    def update_value(self, value, display):
        self.bpm = value
        self.__update_midi()
        self.__show_edit(display)

    def switch(self, display):
        self.__update_midi()
        if (self.in_edit):
            self.__show_edit(display)
        else:
            self.show_view(display)

    def next(self):
        return None
    
    def __show_edit(self, display):
        self.__show_current(display,
            colour=(32,255,32) if self.bpm == self.saved_bpm else (127,0,0))

    def __show_current(self, display, colour=(255,255,255)):
        display.show_text(
            str(self.bpm),
            line2_text="BPM",
            colour=colour,
            line2_indent=5)

    def __update_midi(self):
        self.applied = True
        value14 = round((self.bpm - 40) / 440 * 16383)
        self.midi_out.send_control_change(MIDI_CHANNEL, MIDI_CC_NRPN_LSB, 6)
        self.midi_out.send_control_change(MIDI_CHANNEL, MIDI_CC_NRPN_MSB, 38)
        self.midi_out.send_control_change(MIDI_CHANNEL, MIDI_CC_DATA_MSB, value14 >> 7)
        self.midi_out.send_control_change(MIDI_CHANNEL, MIDI_CC_DATA_LSB, value14 & 0x7f)

