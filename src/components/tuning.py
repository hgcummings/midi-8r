MIDI_CHANNEL = 0 # Zero-indexed, so this is MIDI Channel 1
MIDI_CC_TUNER_ON_OFF = 16

tunings = ["E std.","drp D"]

class Tuning:
    """
    Component for selecting the tuning associated with the current patch

    When a patch is first loaded, if the tuning changes, raises an alert and enables the tuner
    """
    format = "B"

    def __init__(self, midi_out):
        self.midi_out = midi_out

        self.last_acknowledged_tuning = 0
        self.alert = False

    def load(self, data):
        self.index = data[0]
        self.saved_index = self.index
        if (self.index != self.last_acknowledged_tuning):
            self._set_alert()
        elif (self.alert):
            self.clear_alert()

    def show_view(self, display):
        display.show_text(tunings[self.index])

    def _set_alert(self):
        self.alert = True
        self.midi_out.send_control_change(MIDI_CHANNEL, MIDI_CC_TUNER_ON_OFF, 127)

    def clear_alert(self):
        self.alert = False
        self.last_acknowledged_tuning = self.index
        self.midi_out.send_control_change(MIDI_CHANNEL, MIDI_CC_TUNER_ON_OFF, 0)

    def edit(self, display):
        self.__show_edit(display)
        return (0, self.index, len(tunings) - 1)

    def update_value(self, value, display):
        self.index = value
        self.__show_edit(display)

    def switch(self, *_):
        pass

    def next(self):
        return None

    def save(self):
        self.last_acknowledged_tuning = self.index
        self.saved_index = self.index
        return (self.index,)
        
    def __show_edit(self, display):
        display.show_text(tunings[self.index],
            colour=(32,255,32) if self.index == self.saved_index else (127,0,0))
