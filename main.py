from cores.diag import Diagnostic
from ports.rgb_matrix import RgbMatrix
from ports.shell_midi import ShellMidi
from ports.encoder import Encoder
from adapters.storage.file import FileStorage
from adapters.display import Display
from config import *

midi = ShellMidi()
matrix = RgbMatrix(RGB_MATRIX_PIN_DT, RGB_MATRIX_ROWS, RGB_MATRIX_COLS)

core = Diagnostic(
    midi,
    Encoder(ENCODER_PIN_BTN, ENCODER_PIN_CLK, ENCODER_PIN_DT, OUTPUT_PATCH_RANGE - 1),
    FileStorage('/storage.bin'),
    Display(matrix)
)