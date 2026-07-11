import json

from components.props.cerberus.cab_sim import CabSim
from components.props.cerberus.reverb import Reverb
from components.props.tuning import Tuning
from components.props.guitar import Guitar

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

with open(__file__.replace("config.py", "guitars.json"), encoding="utf8") as f:
    guitars = json.load(f)

def init_components(midi):
    return [CabSim(midi), Reverb(midi), Tuning(midi), Guitar(guitars)]