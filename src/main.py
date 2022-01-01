from cores.diag import Diagnostic
from ports.external_midi import ExternalMidi
from ports.rgb_matrix import RgbMatrix
from ports.encoder import Encoder
from adapters.storage.file import FileStorage
from adapters.midi_thru import MidiThru
from adapters.display import Display
from config import *

matrix = RgbMatrix(RGB_MATRIX_PIN_DT, RGB_MATRIX_ROWS, RGB_MATRIX_COLS)

core = Diagnostic(
    MidiThru(ExternalMidi()),
    Encoder(ENCODER_PIN_BTN, ENCODER_PIN_CLK, ENCODER_PIN_DT, OUTPUT_PATCH_RANGE - 1),
    FileStorage('/storage.bin'),
    Display(matrix)
)