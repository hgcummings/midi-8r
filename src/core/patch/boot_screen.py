class BootScreen:
    """Simple component to display a message until the first patch has been loaded"""
    def edit(self, display):
        display.show_text("Patch")
        return (0,0,0)

    def update_value(self, *_):
        pass

    def switch(self, *_):
        pass

    def next(self):
        return self
