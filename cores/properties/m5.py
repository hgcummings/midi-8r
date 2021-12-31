from adafruit_midi.control_change import ControlChange
from adafruit_midi.program_change import ProgramChange

MIDI_CHANNEL = 1 # Zero-indexed, so this is Channel 2
MIDI_CC_ON_OFF = 11 # TODO:2 Check if this is zero-indexed and should be 10

MIN_PRESET = 1
MAX_PRESET = 24

class M5:
    format = "b"
    alert = False

    def __init__(self, midi, control, display):
        self.midi = midi
        self.control = control
        self.display = display

    def load(self, data):
        if (data[0] == 0):
            # No patch saved; loaded empty data
            self.preset = 1
            self.init_on = False
        else:
            self.preset = abs(data[0])
            self.init_on = (self.preset == data[0]) # Init off stored as negative

        self.saved_preset = self.preset

        # TODO:1 Could specify channel inside message object instead?
        self.midi.send_message(ProgramChange(self.preset - 1), channel=MIDI_CHANNEL)
        self.midi.send_message(ControlChange(MIDI_CC_ON_OFF, 127 if self.init_on else 0), channel=MIDI_CHANNEL)

    def show(self):
        self.display.show_text("P{}".format(self.preset))

    def edit(self):
        self.control.set_range(MIN_PRESET, MAX_PRESET)
        self.control.set_value(self.preset)
        self.__display_edit()

    def next(self):
        return False

    def update_value(self, value):
        self.preset = value
        self.__display_edit()

    def save(self):
        self.saved_preset = self.preset
        return (self.preset * (1 if self.init_on else -1),)
        
    def __display_edit(self):
        self.display.show_text("P{}".format(self.preset),
            colour=(32,255,32) if self.preset == self.saved_preset else (127,0,0))
