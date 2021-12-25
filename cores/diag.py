import adafruit_midi
from adafruit_midi.program_change import ProgramChange

class Diagnostic:
    def __init__(self, midi, control, storage, display) -> None:
        self.midi = midi
        self.control = control
        self.storage = storage
        self.display = display

        self.midi.observe_midi_messages(self.on_midi_message)

    def on_midi_message(self, message):
        if (isinstance(message, ProgramChange)):
            self.display.show_patch(message.patch)