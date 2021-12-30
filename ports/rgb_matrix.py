from machine import Pin
import rp2

# The RGB matrix pixels are _very_ bright, so reduce all the intensities by this factor
DIM_FACTOR = 16

# Configure the number of WS2812 LEDs.
NUM_ROWS = 10
NUM_COLS = 16

@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    label("do_zero")
    nop()                   .side(0)    [T2 - 1]
    wrap()

class RgbMatrix:
    def __init__(self, pin, rows, cols):
        self.sm = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(pin))
        self.sm.active(1)
        self.buffer = [0 for _ in range(rows * cols)]
        self.show_buffer()
        self.rows = rows
        self.cols = cols

    def show_pixels(self, pixels):
        for i in range(NUM_ROWS):
            for j in range(NUM_COLS):
                if i < len(pixels) and j < len(pixels[i]):
                    self.buffer[(i * NUM_COLS) + j] = (
                        ((pixels[i][j][0] // DIM_FACTOR) << 8) |
                        ((pixels[i][j][1] // DIM_FACTOR) << 16) |
                        (pixels[i][j][2] // DIM_FACTOR)
                    )
                else:
                    self.buffer[(i * NUM_COLS) + j] = 0
        self.show_buffer()

    def clear(self):
        for i in range(self.rows * self.cols):
            self.buffer[i] = 0
        self.show_buffer()

    def show_buffer(self):
        for pixel in self.buffer:
            self.sm.put(pixel, 8)

