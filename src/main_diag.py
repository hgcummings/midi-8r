from cores.diag import Diagnostic
from ports.external_midi import ExternalMidi
from adapters.midi_thru import MidiThru
from ports.rgb_matrix import RgbMatrix
from adapters.storage.file import FileStorage
from ports.control import Control
from adapters.display import Display
from config import *

display = Display(RgbMatrix(RGB_MATRIX_PIN_DT, RGB_MATRIX_ROWS, RGB_MATRIX_COLS, dim_factor=64))

core = Diagnostic(
    MidiThru(ExternalMidi(MIDI_UART_PIN_TX, MIDI_UART_PIN_RX, MIDI_CHANNEL_IN, MIDI_CHANNEL_OUT)),
    Control(ENCODER_PIN_BTN, ENCODER_PIN_CLK, ENCODER_PIN_DT, FOOTSWITCH_PIN),
    FileStorage("/storage/patches/diag_all"),
    display
)
