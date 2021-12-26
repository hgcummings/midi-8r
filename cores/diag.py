from adafruit_midi.program_change import ProgramChange
from adapters.control import EncoderEvent
from config import *

class Diagnostic:
    def __init__(self, midi, control, storage, display) -> None:
        self.midi = midi
        self.control = control
        self.storage = storage
        self.display = display

        self.display.show_text("DIAG")

        self.midi.observe_messages(self.on_midi_message)
        self.control.observe_encoder(self.on_encoder_event)

        self.input_patch = None
        self.output_patch = None

    def on_midi_message(self, message):
        if (isinstance(message, ProgramChange)):
            self.update_patches(message.patch, message.patch)

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
            self.display.show_patches(self.input_patch, self.output_patch)

    def on_encoder_event(self, event):
        if (self.output_patch != None):
            if (event == EncoderEvent.INCREMENT):
                self.update_patches(self.input_patch, (self.output_patch + 1))
            elif (event == EncoderEvent.DECREMENT):
                self.update_patches(self.input_patch, (self.output_patch - 1))