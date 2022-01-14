from machine import UART, Pin, Timer
from .midi_stream_reader import MidiStreamReader
from .midi_message_types import *

MIDI_BAUD_RATE = 31250
READ_INTERVAL_MS = 100
RX_BUFFER_SIZE = 4096 # Should be greater than MIDI_BAUD_RATE / READ_INTERVAL_MS

class MidiOverUart:
    """Provides external MIDI in/out via UART"""
    def __init__(self, tx_pin, rx_pin, out_channel, in_channel):
        self.uart = UART(0,baudrate=MIDI_BAUD_RATE,tx=Pin(tx_pin),rx=Pin(rx_pin), rxbuf=RX_BUFFER_SIZE)
        self.in_channel = in_channel
        self.out_channel = out_channel
        self.rx_buf = memoryview(bytearray(256))
        self.tx_buf = memoryview(bytearray(3))

    def __recv_midi(self, *_):
        while self.uart.any():
            length = self.uart.readinto(self.rx_buf)
            self.midi_reader.consume(self.rx_buf[:length])

    def __send_message(self, msg_type, channel, data, data2=None):
        if (channel == None):
            channel = self.out_channel

        self.tx_buf[0] = (msg_type << 4) | channel
        self.tx_buf[1] = data
        length = 2
        if (data2 != None):
            length = 3
            self.tx_buf[2] = data2

        self.uart.write(self.tx_buf[:length])

    def register_handler(self, handler):
        self.midi_reader = MidiStreamReader(self.in_channel, handler)

        # UART.irq isn't implemented for rp2 yet, so use polling rather than interrupt
        #
        # Note: although we don't need to reference the timer again, it's important to
        # store it in an instance attribute so that it doesn't get GC'd
        self.timer = Timer(-1)
        self.timer.init(period=READ_INTERVAL_MS, mode=Timer.PERIODIC, callback=self.__recv_midi)

    def send_raw_bytes(self, raw_bytes):
        self.uart.write(raw_bytes)

    def send_program_change(self, patch, channel=None):
        self.__send_message(PROGRAM_CHANGE, channel, patch)

    def send_control_change(self, controller, value, channel=None):
        self.__send_message(CONTROL_CHANGE, channel, controller, value)
