from cores.diag import Diagnostic
from cores.patch import PatchCore
from ports.gui import Application
from adapters.storage.file import FileStorage
from adapters.display import Display
import os
from config import *

app = Application(RGB_MATRIX_ROWS, RGB_MATRIX_COLS)

storage_root = os.path.dirname(__file__)
core = PatchCore(storage_root, app, app, Display(app))

app.show_ui()