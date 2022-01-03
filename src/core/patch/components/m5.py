from adafruit_midi.control_change import ControlChange
from adafruit_midi.program_change import ProgramChange

MIDI_CHANNEL = 1 # Adafruit MIDI library is zero-indexed, so this is MIDI Channel 2
MIDI_CC_ON_OFF = 11

MIN_PRESET = 1
MAX_PRESET = 24

class M5:
    """
    Component for selecting the preset on the Line 6 M5 pedal, which supports 24 patches

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

    def show_view(self, display):
        self.__show_current(display)

    def edit(self, display):
        self.__show_edit(display)
        return (MIN_PRESET, self.preset, MAX_PRESET)

    def update_value(self, value, display):
        self.preset = value
        self.__show_edit(display)
        self.__update_midi()

    def switch(self, display):
        self.init_on = not self.init_on
        self.__update_midi()
        self.__show_edit(display)

    def next(self):
        return None

    def save(self):
        self.saved_preset = self.preset
        self.saved_init_on = self.init_on
        return (self.preset * (1 if self.init_on else -1),)

    def __show_edit(self, display):
        self.__show_current(display,
            colour=(32,255,32) if self.preset == self.saved_preset and self.init_on == self.saved_init_on else (127,0,0))

    def __show_current(self, display, colour=(255,255,255)):
        display.show_text(
            "P{}".format(self.preset),
            line2_text="(on)" if self.init_on else "(off)",
            line2_indent=1,
            colour=colour)

    def __update_midi(self):
        self.midi_out(ProgramChange(self.preset - 1), channel=MIDI_CHANNEL)
        self.midi_out(ControlChange(MIDI_CC_ON_OFF, 127 if self.init_on else 0), channel=MIDI_CHANNEL)
