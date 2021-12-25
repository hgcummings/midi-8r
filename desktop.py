from cores.diag import Diagnostic
from adapters.gui import Application
from adapters.display import Display

app = Application()

core = Diagnostic(app, app, app, Display(app))

app.show_ui()