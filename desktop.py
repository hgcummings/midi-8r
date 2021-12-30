from cores.diag import Diagnostic
from ports.gui import Application
from adapters.storage.file import FileStorage
from adapters.display import Display
import os
from config import *

app = Application(RGB_MATRIX_ROWS, RGB_MATRIX_COLS)

storage_path = os.path.join(os.path.dirname(__file__), "storage.bin")

core = Diagnostic(app, app, FileStorage(storage_path), Display(app))
app.show_ui()