import tkinter as tk
import adafruit_midi
from adafruit_midi.program_change import ProgramChange

width = 16
height = 10
scale = 20

def rgb_color(rgb):
    return "#%02x%02x%02x" % rgb  

class Application:
    def __init__(self):
        self.app = tk.Tk()

        self.display = tk.Canvas(self.app, width=scale*width, height=scale*height, background="black")
        self.display.grid(column = 0, columnspan=2, row=0)

        self.midi_in = tk.Entry(self.app)
        self.midi_in.grid(column = 1, row = 1)

        midi_in_send = tk.Button(self.app, text="Send", command=self.send_midi_in)
        midi_in_send.grid(column = 1, row = 2)

        self.midi_observer = None

    def show_ui(self):
        self.app.mainloop()

    def observe_midi_messages(self, observer):
        self.midi_observer = observer

    def show_pixels(self, pixels):
        self.display.delete("all")
        for y, row in enumerate(pixels):
            for x, pixel in enumerate(row):
                self.display.create_rectangle(scale * x, scale * y, scale * (1+x) - 1, scale * (1+y) - 1, fill=rgb_color(pixel))

    def send_midi_in(self):
        if (self.midi_observer):
            self.midi_observer(ProgramChange(int(self.midi_in.get())))