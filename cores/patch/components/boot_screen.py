class BootScreen:
    def edit(self, display):
        display.show_bitmap("patch.bin", (255,255,255))
        return (0,0,0)

    def update_value(self, *_):
        pass

    def switch(self, *_):
        pass

    def next(self):
        return self
