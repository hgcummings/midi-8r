from .graphics.font import render_line

class Display:
    def __init__(self, pixel_display):
        self.pixel_display = pixel_display

    def show_patches(self, patch_in, patch_out, saved):
        self.pixel_display.show_pixels(
            render_line("▶" + str(patch_in), (255,255,255)) +
            render_line("◀" + str(patch_out), (64, 255, 64) if saved else (255, 64, 64)))

    def show_text(self, text):
        self.pixel_display.show_pixels(render_line(text, (255, 255, 255)))

class ConsoleDisplay:
    def show_pixels(self, pixels):
        for row in pixels:
            line = [" " if c == (0,0,0) else "=" for c in row]
            print("".join(line))