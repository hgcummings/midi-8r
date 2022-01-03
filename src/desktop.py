import sys
from pathlib import Path

from cores.diag import Diagnostic
from cores.patch import PatchCore
from adapters.storage.file import FileStorage
from adapters.display import Display
from ports.emulated.gui import Application

from config import *

app = Application(RGB_MATRIX_ROWS, RGB_MATRIX_COLS)

storage_root = Path(Path(__file__).resolve().parent.parent, "storage")

if len(sys.argv) > 1 and sys.argv[1] == "diag":
    core = Diagnostic(app, app, FileStorage(Path(storage_root, "patches", "diag_all")), Display(app))
else:
    core = PatchCore(storage_root, app, app, Display(app))

app.show_ui()