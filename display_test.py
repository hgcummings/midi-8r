from adapters.display import ConsoleDisplay
from adapters.graphics.font import render_line

console_display = ConsoleDisplay()

console_display.show_pixels(render_line("TEST", (255,255,255)))

