from adafruit_midi.program_change import ProgramChange
from config import *

class Diagnostic:
    def __init__(self, midi, control, storage, display) -> None:
        self.midi = midi
        self.control = control
        self.storage = storage
        self.display = display

        self.display.show_text("DIAG")

        self.input_patch = None
        self.output_patch = None
        self.midi.observe_messages(self.on_midi_message)

        self.control.observe_value(self.on_value_change)
        self.control.observe_button(self.on_button_change)

    def on_midi_message(self, message):
        if (isinstance(message, ProgramChange)):
            preset = self.storage.get_preset(message.patch)
            self.update_patches(message.patch, preset)
            self.control.set_value(preset)

    def update_patches(self, input_patch, output_patch):
        changed = False

        if (input_patch != self.input_patch):
            self.input_patch = input_patch
            changed = True

        output_patch = output_patch % OUTPUT_PATCH_RANGE
        if (output_patch != self.output_patch):
            self.output_patch = output_patch
            self.midi.send_message(ProgramChange(output_patch))
            changed = True

        if changed:
            self.display.show_patches(
                self.input_patch,
                self.output_patch,
                self.output_patch == self.storage.get_preset(self.input_patch))

    def on_button_change(self, pressed):
        if (pressed and self.input_patch != None):
            self.storage.set_preset(self.input_patch, self.output_patch)
            self.display.show_patches(self.input_patch, self.output_patch, True)

    def on_value_change(self, value):
        if (self.input_patch != None):
            self.update_patches(self.input_patch, value)