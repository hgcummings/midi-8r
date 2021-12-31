from adafruit_midi.program_change import ProgramChange
from adafruit_midi.control_change import ControlChange

class ShellMidi:
    def __init__(self):
        self.midi_observer = None
    
    def pc(self, value):
        patch = int(value)
        if (patch >= 0 and patch < 128):
            if (self.midi_observer):
                self.midi_observer(ProgramChange(patch))
        else:
            print("Invalid patch")
    
    def observe_messages(self, observer):
        self.midi_observer = observer
        
    def send_message(self, message, channel=0):
        # TODO:1 Could specify channel inside message object instead?
        if (isinstance(message, ProgramChange)):
            print("C{}PC{}".format(channel, message.patch))
        elif (isinstance(message, ControlChange)):
            print("C{}CC{}V{}".format(channel, message.control, message.value))
        else:
            print("[msg]")