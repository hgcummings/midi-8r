from machine import UART, Pin, Timer
from adafruit_midi import MIDI

class ExternalMidi:
    """Provides external MIDI in/out via UART"""
    def __init__(self, tx_pin, rx_pin, out_channel, in_channel):
        uart = UART(0,baudrate=31250,tx=Pin(tx_pin),rx=Pin(rx_pin))
        self.midi = MIDI(midi_in=uart,midi_out=uart,in_channel=in_channel,out_channel=out_channel)
        self.midi_observer = None

        # UART.irq isn't implemented for rp2 yet, so use polling rather than interrupt
        #
        # Note: although we don't need to reference the timer again, it's important to
        # store it in an instance attribute so that it doesn't get GC'd
        self.timer = Timer(-1)
        self.timer.init(period=100, mode=Timer.PERIODIC, callback=self.recv_midi)
        
    def recv_midi(self, _):
        while(True):
            msg = self.midi.receive()
            if (msg == None):
                break
            elif (self.midi_observer != None):
                self.midi_observer(msg)
                
    # Interface implementation
    def observe_messages(self, observer):
        self.midi_observer = observer

    def send_message(self, msg, channel=None):
        self.midi.send(msg, channel)
