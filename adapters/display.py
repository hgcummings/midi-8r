from .graphics.font import render_line

class Display:
    def __init__(self, pixel_display):
        self.pixel_display = pixel_display

    def show_patch(self, patch):
        self.pixel_display.show_pixels(render_line("P" + str(patch), (255,255,255)))

class ConsoleDisplay:
    def show_pixels(self, pixels):
        for row in pixels:
            line = [" " if c == (0,0,0) else "=" for c in row]
            print("".join(line))