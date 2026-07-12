from .text import render_line

class Display:
    def __init__(self, pixel_display):
        self.pixel_display = pixel_display

    def clear(self):
        self.pixel_display.clear_buffer()
        self.pixel_display.show_buffer()

    def show_text(self, text, line2_text=None, colour=None, indent=0, line2_indent=0, line2_colour=None):
        if colour is None:
            colour = (255, 255, 255)
        self.pixel_display.clear_buffer()
        if line2_text:
            render_line(self.pixel_display, indent, 0, text, colour)
            render_line(self.pixel_display, line2_indent, 5, line2_text, line2_colour if line2_colour is not None else colour)
        else:
            render_line(self.pixel_display, indent, 2, text, colour)
        self.pixel_display.show_buffer()

    def show_image(self, width, height, image):
        self.pixel_display.clear_buffer()

        offset_x = (self.pixel_display.cols - width) // 2
        offset_y = (self.pixel_display.rows - height) // 2

        for y in range(height):
            for x in range(width):
                self.pixel_display.set_pixel(x + offset_x, y + offset_y, *image[y][x])
        self.pixel_display.show_buffer()

