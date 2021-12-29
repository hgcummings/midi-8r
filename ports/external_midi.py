from machine import UART, Pin, Timer
from adafruit_midi import MIDI

class ExternalMidi:
    def __init__(self, tx_pin, rx_pin, out_channel, in_channel):
        uart = UART(0,baudrate=31250,tx=Pin(tx_pin),rx=Pin(rx_pin))
        self.midi = MIDI(midi_in=uart,midi_out=uart,in_channel=in_channel,out_channel=out_channel)
        self.midi_observer = None

        # UART.irq isn't implemented for rp2 yet, so use polling rather than interrupt
        timer = Timer(-1, mode=Timer.PERIODIC,period=100,callback=self.recv_midi)
        
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

    def send_message(self, msg):
        self.midi.send(msg)