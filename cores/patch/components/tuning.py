import json
from adafruit_midi.control_change import ControlChange

MIDI_CC_TUNER_ON_OFF = 16

tunings = ["E std.","drpD"]

font_path = __file__.replace(".py", "_font.json")
with open(font_path, encoding="utf8") as f:
    font = json.load(f)

class Tuning:
    format = "B"

    def __init__(self, midi):
        self.midi = midi

        self.last_acknowledged_tuning = 0
        self.alert = False

    def load(self, data):
        self.index = data[0]
        self.saved_index = self.index
        if (self.index != self.last_acknowledged_tuning):
            self._set_alert()
        elif (self.alert):
            self.clear_alert()

    def save(self):
        return (self.index,)

    def show_view(self, display):
        display.show_text(tunings[self.index], font)

    def _set_alert(self):
        self.alert = True
        self.midi.send_message(ControlChange(MIDI_CC_TUNER_ON_OFF, 127))

    def clear_alert(self):
        self.alert = False
        self.last_acknowledged_tuning = self.index
        self.midi.send_message(ControlChange(MIDI_CC_TUNER_ON_OFF, 0))

    def edit(self, display):
        self.__show_edit(display)
        return (0, self.index, len(tunings) - 1)

    def next(self):
        return None

    def update_value(self, value, display):
        self.index = value
        self.__show_edit(display)

    def save(self):
        self.last_acknowledged_tuning = self.index
        self.saved_index = self.index
        return (self.index,)
        
    def __show_edit(self, display):
        display.show_text(tunings[self.index], font,
            colour=(32,255,32) if self.index == self.saved_index else (127,0,0))