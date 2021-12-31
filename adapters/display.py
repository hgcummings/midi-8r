from .graphics.text import render_line
from .graphics.text import default_font
import struct

class Display:
    def __init__(self, pixel_display):
        self.pixel_display = pixel_display

    def clear(self):
        self.pixel_display.clear_buffer()
        self.pixel_display.show_buffer()

    def show_text(self, text, font=default_font, colour=(255,255,255)):
        self.pixel_display.clear_buffer()
        render_line(self.pixel_display, 0, 2, text, colour, font)
        self.pixel_display.show_buffer()

    def show_patches(self, patch_in, patch_out, saved):
        self.pixel_display.clear_buffer()
        render_line(self.pixel_display, 0, 0, "▶{}".format(patch_in), (255,255,255))
        render_line(self.pixel_display, 0, 5, "◀{}".format(patch_out),
                                        (32, 255, 32) if saved else (127, 0, 0))
        self.pixel_display.show_buffer()

    def show_bitmap(self, filename, colour):
        self.pixel_display.clear_buffer()
        bitmap_path = __file__.replace("display.py", "graphics/bitmaps/{}".format(filename))

        with open(bitmap_path, "rb") as f:
            for y in range(self.pixel_display.rows):
                bytes = f.read(2)
                line = struct.unpack(">H", bytes)[0]
                for x in range(self.pixel_display.cols):
                    bit = 1 << (self.pixel_display.cols - 1 - x)
                    if (bit & line):
                        self.pixel_display.set_pixel(x, y, colour[0], colour[1], colour[2])

        self.pixel_display.show_buffer()