from cores.diag import Diagnostic
from ports.gui import Application
from adapters.storage.file import FileStorage
from adapters.display import Display

app = Application()

with open("storage.bin", "r+b") as f:
    core = Diagnostic(app, app, FileStorage(f.fileno()), Display(app))
    app.show_ui()