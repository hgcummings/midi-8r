from adapters.noop.storage import NoOpStorage
from cores.diag import Diagnostic
from ports.rgb_matrix import RgbMatrix
from ports.shell_midi import ShellMidi
from ports.encoder import Encoder
from adapters.display import Display
from adapters.noop import *
from config import *

midi = ShellMidi()

core = Diagnostic(
    midi,
    Encoder(ENCODER_PIN_A, ENCODER_PIN_B, OUTPUT_PATCH_RANGE - 1),
    NoOpStorage(),
    Display(RgbMatrix(RGB_MATRIX_PIN_NO))
)