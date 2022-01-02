from adafruit_midi import MIDIMessage
from adafruit_midi.midi_message import MIDIUnknownEvent

class MidiThru:
    def __init__(self, midi_port):
        self.midi_observer = None
        self.midi_port = midi_port

        self.midi_port.observe_messages(self.on_message)

    def observe_messages(self, observer):
        self.midi_observer = observer

    def on_message(self, msg):
        if (self.midi_observer):
            self.midi_observer(msg)
        # adafruit_midi doesn't seem to have a way of forwarding unrecognised messages,
        # so we can't easily offer true MIDI through, but just forward what we can.
        if not (msg is MIDIUnknownEvent):
            self.midi_port.send_message(msg, msg.channel)

    def send_message(self, msg, channel=0):
        self.midi_port.send_message(msg, channel)