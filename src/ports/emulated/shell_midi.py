from adafruit_midi.program_change import ProgramChange
from adafruit_midi.control_change import ControlChange

class ShellMidi:
    def __init__(self):
        self.midi_observer = None
    
    def pc(self, value):
        patch = int(value)
        if (patch >= 0 and patch < 128):
            if (self.handler):
                self.handler.on_program_change(0, patch)
        else:
            print("Invalid patch")
    
    def register_handler(self, handler):
        self.handler = handler

    def send_program_change(self, channel, patch):
        print("C{}PC{}".format(channel, patch))
        
    def send_control_change(self, channel, controller, value):
        print("C{}CC{}V{}".format(channel, controller, value))

    def send_raw_bytes(self, raw_bytes):
        print("[Length: {}]", len(raw_bytes))
