from cores.diag import Diagnostic
from ports.rgb_matrix import RgbMatrix
from ports.shell_midi import ShellMidi
from ports.encoder import Encoder
from adapters.storage.transient import TransientStorage
from adapters.display import Display
from adapters.noop import *
from config import *

midi = ShellMidi()

core = Diagnostic(
    midi,
    Encoder(ENCODER_PIN_BTN, ENCODER_PIN_CLK, ENCODER_PIN_DT, OUTPUT_PATCH_RANGE - 1),
    TransientStorage(),
    Display(RgbMatrix(RGB_MATRIX_PIN_NO))
)