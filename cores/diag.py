class Diagnostic:
    def __init__(self, midi, control, storage, display) -> None:
        self.midi = midi
        self.control = control
        self.storage = storage
        self.display = display

        self.midi.observe_prog_change(self.on_prog_change)

    def on_prog_change(self, value):
        self.display.show_preset(value)