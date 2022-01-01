class BootScreen:
    def edit(self, display):
        display.show_text("Patch")
        return (0,0,0)

    def update_value(self, *_):
        pass

    def switch(self, *_):
        pass

    def next(self):
        return self
