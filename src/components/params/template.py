class Parameter:
    """
    Template for implementing a parameter — a single editable value stored per patch.

    Define the byte structure for storing this parameter's data.
    See https://docs.python.org/3/library/struct.html
    """
    format = "B"

    def __init__(self, midi_out):
        self.midi_out = midi_out

    def load(self, data):
        """
        Load state from `data`, a tuple unpacked according to `format`.
        May send MIDI to update external pedals with the loaded settings.
        May set self.alert = True if a change requires user intervention
        (e.g. switching guitar) that cannot be handled automatically via MIDI.
        """
        self.state = data[0]
        self.saved_state = self.state

    def save(self):
        """Return a tuple of this parameter's data, in `format` order."""
        return (self.state,)

    def value_range(self):
        """Return (min, current, max) for the rotary encoder."""
        return (0, self.state, 255)

    def update_value(self, value):
        """Update state to the encoder value. May send MIDI."""
        self.state = value

    def switch(self):
        """Respond to the footswitch. No-op if not applicable."""
        pass

    def has_changed(self):
        """Return True if current state differs from last saved state."""
        return self.state != self.saved_state

    def render(self, display, colour=None):
        """Render current state to the display using the given colour."""
        display.show_text(str(self.state), colour=colour)

    # Optional: implement advance() to support multi-step editing.
    # Called by ParameterScreen after each button press. Return True to
    # advance to the next editing step, False when editing is complete.
    #
    # def advance(self):
    #     return False

    # Optional: implement alert and clear_alert() for changes requiring
    # user intervention. Set self.alert = True in load() to flag an alert.
    # ParameterScreen will step through clear_alert() calls on edit entry.
    # PresetMenu will prioritise this parameter in its display while alert is set,
    # and clear_alert() will be called once per footswitch press.
    #
    # def clear_alert(self):
    #     self.alert = False
