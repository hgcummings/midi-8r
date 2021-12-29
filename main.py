from adapters.noop.control import NoOpControl
from adapters.noop.storage import NoOpStorage
from cores.diag import Diagnostic
from ports.rgb_matrix import RgbMatrix
from ports.shell_midi import ShellMidi
from adapters.display import Display
from adapters.noop import *
from config import *

midi = ShellMidi()

core = Diagnostic(midi, NoOpControl(), NoOpStorage(), Display(RgbMatrix(RGB_MATRIX_PIN_NO)))