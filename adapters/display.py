from .graphics.font import render_line

class Display:
    def __init__(self, pixel_display):
        self.pixel_display = pixel_display

    def clear(self):
        self.pixel_display.clear_buffer()
        self.pixel_display.show_buffer()

    def show_text(self, text):
        self.pixel_display.clear_buffer()
        render_line(self.pixel_display, 0, 2, text, (255, 255, 255))
        self.pixel_display.show_buffer()

    def show_patches(self, patch_in, patch_out, saved):
        self.pixel_display.clear_buffer()
        render_line(self.pixel_display, 0, 0, "▶{}".format(patch_in), (255,255,255))
        render_line(self.pixel_display, 0, 5, "◀{}".format(patch_out),
                                        (32, 255, 32) if saved else (127, 0, 0))
        self.pixel_display.show_buffer()
