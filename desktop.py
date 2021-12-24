from cores.diag import Diagnostic
from adapters.gui import Application

app = Application()

core = Diagnostic(app, app, app, app)

app.show_ui()