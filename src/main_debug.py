from cores.patch import PatchCore
from ports.shell_midi import ShellMidi
from ports.rgb_matrix import RgbMatrix
from ports.control import Control
from adapters.display import Display
from config import *

midi = ShellMidi()
display = Display(RgbMatrix(RGB_MATRIX_PIN_DT, RGB_MATRIX_ROWS, RGB_MATRIX_COLS, dim_factor=16))

core = PatchCore(
    "/storage",
    midi,
    Control(ENCODER_PIN_BTN, ENCODER_PIN_CLK, ENCODER_PIN_DT, FOOTSWITCH_PIN),
    display
)
