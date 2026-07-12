import json

from components.parameter_screen import ParameterScreen
from components.props.cerberus.cab_sim import CabSim
from components.props.cerberus.reverb import Reverb
from components.props.cerberus.post_boost import PostBoost
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

def direct_props(midi):
    return [
        CabSim(midi),
        Reverb(midi),
        PostBoost(midi)
    ]

def preset_props(midi):
    return [
        ParameterScreen(CabSim(midi)),
        ParameterScreen(Reverb(midi)),
        ParameterScreen(Tuning(midi)),
        ParameterScreen(Guitar(guitars))]
