from cores.patch import PatchCore
from ports.gui import Application
from adapters.storage.file import FileStorage
from adapters.display import Display

from pathlib import Path
from config import *

app = Application(RGB_MATRIX_ROWS, RGB_MATRIX_COLS)

storage_root = Path(__file__).resolve().parent.parent
core = PatchCore(storage_root, app, app, Display(app))

app.show_ui()