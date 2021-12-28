from adapters.noop.control import NoOpControl
from adapters.noop.midi import NoOpMidi
from adapters.noop.storage import NoOpStorage
from cores.diag import Diagnostic
from ports.rgb_matrix import RgbMatrix
from adapters.display import Display
from adapters.noop import *
from config import *

matrix = RgbMatrix(RGB_MATRIX_PIN_NO)

core = Diagnostic(NoOpMidi(), NoOpControl(), NoOpStorage(), Display(matrix))