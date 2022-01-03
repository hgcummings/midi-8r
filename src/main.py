from cores.patch import PatchCore
from ports.hardware.external_midi import ExternalMidi
from ports.hardware.control_panel import ControlPanel
from ports.hardware.rgb_matrix import RgbMatrix
from adapters.midi_thru import MidiThru
from adapters.display import Display
from config import *

core = PatchCore(
    "/storage",
    MidiThru(ExternalMidi(MIDI_UART_PIN_TX, MIDI_UART_PIN_RX, MIDI_CHANNEL_IN, MIDI_CHANNEL_OUT)),
    ControlPanel(ENCODER_PIN_BTN, ENCODER_PIN_CLK, ENCODER_PIN_DT, FOOTSWITCH_PIN),
    Display(RgbMatrix(RGB_MATRIX_PIN_DT, RGB_MATRIX_ROWS, RGB_MATRIX_COLS))
)
