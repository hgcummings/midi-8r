from cores.diag import Diagnostic
from ports.rgb_matrix import RgbMatrix
from ports.external_midi import ExternalMidi
from ports.encoder import Encoder
from adapters.storage.file import FileStorage
from adapters.display import Display
from adapters.noop import *
from config import *

core = Diagnostic(
    ExternalMidi(MIDI_UART_PIN_TX, MIDI_UART_PIN_RX, MIDI_CHANNEL_OUT, MIDI_CHANNEL_IN),
    Encoder(ENCODER_PIN_BTN, ENCODER_PIN_CLK, ENCODER_PIN_DT, OUTPUT_PATCH_RANGE - 1),
    FileStorage('/storage.bin'),
    Display(RgbMatrix(RGB_MATRIX_PIN_NO))
)