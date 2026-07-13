import json

from components.params.cerberus.cab_sim import CabSim
from components.params.cerberus.reverb import Reverb
from components.params.cerberus.post_boost import PostBoost
from components.params.tuning import Tuning
from components.params.guitar import Guitar

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

def direct_params(midi):
    return [
        CabSim(midi),
        Reverb(midi),
        PostBoost(midi)
    ]

def preset_params(midi):
    return [
        CabSim(midi),
        Reverb(midi),
        Tuning(midi),
        Guitar(guitars)]
