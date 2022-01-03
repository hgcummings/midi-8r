from machine import Pin
import rp2
from .neopixel import ws2812

# Configure the number of WS2812 LEDs.
NUM_ROWS = 10
NUM_COLS = 16

class RgbMatrix:
    def __init__(self, pin, rows, cols, dim_factor=8):
        self.sm = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(pin))
        self.sm.active(1)
        self.buffer = [0 for _ in range(rows * cols)]
        self.show_buffer()
        self.rows = rows
        self.cols = cols
        # The RGB matrix pixels are _very_ bright, so reduce all the intensities by this factor
        self._dim = dim_factor

    def clear_buffer(self):
        for i in range(self.rows * self.cols):
            self.buffer[i] = 0
    
    def set_pixel(self, x, y, r, g, b):
        if (y < self.rows and x < self.cols):
            self.buffer[(y * self.cols) + x] = (
                ((r // self._dim) << 8) | ((g // self._dim) << 16) | (b // self._dim)
            )
    
    def show_buffer(self):
        for pixel in self.buffer:
            self.sm.put(pixel, 8)
