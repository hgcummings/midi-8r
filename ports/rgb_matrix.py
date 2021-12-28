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
    def __init__(self,pin):
        self.sm = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(pin))
        self.sm.active(1)
        self.clear()
        
    def clear(self):
        for i in range(NUM_ROWS):
            for j in range(NUM_COLS):
                self.push_pixel((0,0,0))

    def show_pixels(self, pixels):
        buffer = []
        for i in range(NUM_ROWS):
            for j in range(NUM_COLS):
                if i < len(pixels) and j < len(pixels[i]):
                    buffer.append((pixels[i][j][0] // DIM_FACTOR,
                                   pixels[i][j][1] // DIM_FACTOR,
                                   pixels[i][j][2] // DIM_FACTOR))
                else:
                    buffer.append((0,0,0))
        for value in buffer:
            self.push_pixel(value)

    def push_pixel(self, pixel):
        self.sm.put((pixel[0] << 8) | (pixel[1] << 16) | pixel[2], 8)
