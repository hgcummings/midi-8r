from .graphics.text import render_line
from .graphics.text import default_font
import struct

class Display:
    def __init__(self, pixel_display):
        self.pixel_display = pixel_display

    def clear(self):
        self.pixel_display.clear_buffer()
        self.pixel_display.show_buffer()

    def show_text(self, text, line2_text=None, colour=(255,255,255), indent=0, line2_indent=0):
        self.pixel_display.clear_buffer()
        if line2_text:
            render_line(self.pixel_display, indent, 0, text, colour, default_font)
            render_line(self.pixel_display, line2_indent, 5, line2_text, colour, default_font)
        else:
            render_line(self.pixel_display, indent, 2, text, colour, default_font)
        self.pixel_display.show_buffer()

    def show_image(self, width, height, image):
        self.pixel_display.clear_buffer()

        offset_x = (self.pixel_display.cols - width) // 2
        offset_y = (self.pixel_display.rows - height) // 2

        for y in range(height):
            for x in range(width):
                self.pixel_display.set_pixel(x + offset_x, y + offset_y, *image[y][x])
        self.pixel_display.show_buffer()

    def show_patches(self, patch_in, patch_out, saved):
        self.pixel_display.clear_buffer()
        render_line(self.pixel_display, 0, 0, "▶{}".format(patch_in), (255,255,255))
        render_line(self.pixel_display, 0, 5, "◀{}".format(patch_out),
                                        (32, 255, 32) if saved else (127, 0, 0))
        self.pixel_display.show_buffer()
