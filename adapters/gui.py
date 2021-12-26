import tkinter as tk
from tkinter.constants import DISABLED, NORMAL
from adafruit_midi.program_change import ProgramChange

width = 16
height = 10
scale_x = 15
scale_y = 10

def rgb_color(rgb):
    return "#%02x%02x%02x" % rgb  

class Application:
    def __init__(self):
        self.app = tk.Tk()

        self.display = tk.Canvas(self.app, width=scale_x*(width+2), height=scale_y*(height+2), background="black")
        self.display.grid(column = 0, columnspan=3, row=0)

        midi_out_label = tk.Label(self.app, text="MIDI out")
        midi_out_label.grid(column=0, row=1)
        midi_in_label = tk.Label(self.app, text="MIDI in")
        midi_in_label.grid(column=2,row=1)

        self.midi_out_text = tk.StringVar(self.app)
        midi_out = tk.Entry(self.app, state=DISABLED, textvariable=self.midi_out_text)
        midi_out.grid(column = 0, row = 2)
        
        self.midi_in = tk.Entry(self.app, background="white")
        self.midi_in.grid(column = 2, row = 2)
        midi_in_send = tk.Button(self.app, text="Send", command=self.send_midi_in)
        midi_in_send.grid(column = 2, row = 3)

        self.midi_observer = None

    # MIDI implementation
    def observe_messages(self, observer):
        self.midi_observer = observer

    def send_message(self, message):
        if (isinstance(message, ProgramChange)):
            self.midi_out_text.set("P" + str(message.patch))
        else:
            self.midi_out_text.set("[msg]")

    # Display implementation
    def show_pixels(self, pixels):
        self.display.delete("all")
        for y, row in enumerate(pixels):
            if (y > 9):
                break
            for x, pixel in enumerate(row):
                if (x > 15):
                    break
                self.display.create_rectangle(2 + scale_x * (1+x), scale_y * (1+y), scale_x * (2+x) - 4, scale_y * (2+y) - 2, fill=rgb_color(pixel))

    # UI
    def show_ui(self):
        self.app.mainloop()

    def send_midi_in(self):
        patch = int(self.midi_in.get())
        if (patch >= 0 and patch < 128):
            self.midi_in.configure(background="white")
            if (self.midi_observer):
                self.midi_observer(ProgramChange(patch))
        else:
            self.midi_in.configure(background="red")