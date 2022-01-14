from ports.midi_handler import MidiMessageHandler


OUTPUT_PATCH_RANGE = 24

class Diagnostic(MidiMessageHandler):
    """
    Simple core that maps MIDI program change messages

    Incoming program change messages specify a patch number from 0-127
    
    Allows an output patch to be selected, and stored against the current input patch
    """
    def __init__(self, midi, control, storage, display) -> None:
        self.midi = midi
        self.control = control
        self.storage = storage
        self.display = display

        self.display.show_text("DIAG")

        self.input_patch = None
        self.output_patch = None
        self.midi.register_handler(self)

        self.control.observe_value(self.on_value_change)
        self.control.observe_button(self.on_button)

        self.control.set_range_and_value(0, 0, OUTPUT_PATCH_RANGE - 1)

    def on_program_change(self, patch):
        preset = self.storage.get_preset(patch)
        self.update_patches(patch, preset)
        self.control.set_value(preset)

    def update_patches(self, input_patch, output_patch):
        changed = False

        if (input_patch != self.input_patch):
            self.input_patch = input_patch
            changed = True

        output_patch = output_patch % OUTPUT_PATCH_RANGE
        if (output_patch != self.output_patch):
            self.output_patch = output_patch
            self.midi.send_program_change(output_patch)
            changed = True

        if changed:
            self.display.show_patches(
                self.input_patch,
                self.output_patch,
                self.output_patch == self.storage.get_preset(self.input_patch))

    def on_button(self):
        if (self.input_patch != None):
            self.storage.set_preset(self.input_patch, self.output_patch)
            self.display.show_patches(self.input_patch, self.output_patch, True)

    def on_value_change(self, value):
        if (self.input_patch != None):
            self.update_patches(self.input_patch, value)