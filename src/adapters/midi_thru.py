class MidiThru:
    def __init__(self, midi_port):
        self.midi_port = midi_port

    def register_handler(self, handler):
        self.midi_port.register_handler(MidiThru.__Handler(self.midi_port, handler))

    def send_raw_bytes(self, raw_bytes):
        self.midi_port.send_raw_bytes(raw_bytes)

    def send_program_change(self, patch, channel=None):
        self.midi_port.send_program_change(patch, channel)

    def send_control_change(self, controller, value, channel=None):
        self.midi_port.send_control_change(controller, value)

    class __Handler:
        def __init__(self, midi_out, inner):
            self.midi_out = midi_out
            self.inner = inner

        def on_program_change(self, patch):
            self.midi_out.send_program_change(patch)
            self.inner.on_program_change(patch)
            
        def on_control_change(self, controller, value):
            self.midi_out.send_control_change(controller, value)
            self.inner.on_control_change(controller, value)

        def on_unknown_message(self, raw_bytes):
            self.midi_out.send_raw_bytes(raw_bytes)
            self.inner.on_unknown_message(raw_bytes)
