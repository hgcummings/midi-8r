"""
Primary boot script for running on desktop

Uses emulated hardware presented via a GUI

Loads the fully-featured core by default, but can also load the simpler diagnostic core
"""

import sys
from pathlib import Path

from core.diag import Diagnostic
from core.patch import PatchCore
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