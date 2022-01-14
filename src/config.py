from components.m5 import M5
from components.tuning import Tuning
from components.guitar import Guitar

RGB_MATRIX_ROWS=10
RGB_MATRIX_COLS=16
RGB_MATRIX_PIN_DT=21
ENCODER_PIN_BTN=18
ENCODER_PIN_CLK=19
ENCODER_PIN_DT=20
FOOTSWITCH_PIN=15
MIDI_UART_PIN_TX=16
MIDI_UART_PIN_RX=17
MIDI_CHANNEL_IN=0
MIDI_CHANNEL_OUT=0

def init_components(midi):
    return [M5(midi), Tuning(midi), Guitar()]