from adafruit_midi.program_change import ProgramChange

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
        
    def send_message(self, message):
        if (isinstance(message, ProgramChange)):
            print("P" + str(message.patch))
        else:
            print("[msg]")