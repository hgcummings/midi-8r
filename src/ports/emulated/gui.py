import tkinter as tk
from tkinter.constants import DISABLED
from adafruit_midi.control_change import ControlChange
from adafruit_midi.program_change import ProgramChange
from functools import partial

# Pedal dimensions in mm: 70x110
# Pedal dimensions in px: 308x484
# Pixels per mm: 4.4

# Display dimensions
scale_x = 15
scale_y = 10

def rgb_color(rgb):
    return "#%02x%02x%02x" % rgb  

class Application:
    def __init__(self, rows, cols):
        self.app = tk.Tk()

        pedal = tk.Frame(self.app, width=308, height=484, background="black")
        pedal.grid(column=0, columnspan=3, row=0)

        self.buffer = [[(0,0,0) for x in range(cols)] for y in range(rows)]
        self.rows = rows
        self.cols = cols
        self.display = tk.Canvas(pedal, width=scale_x*(cols+2), height=scale_y*(rows+2), background="black")
        self.display.place(relx=0.5, rely=0.1, anchor = "n")

        encoder_frame = tk.Frame(pedal)
        encoder_decr = tk.Button(encoder_frame, text="<", command=partial(self.change_value, -1))
        encoder_decr.grid(column=0, row=0)
        encoder = tk.Button(encoder_frame, text="O", command=self.press_button)
        encoder.grid(column=1, row=0)
        encoder_decr = tk.Button(encoder_frame, text=">", command=partial(self.change_value, +1))
        encoder_decr.grid(column=2, row=0)
        encoder_frame.place(relx=0.5, rely=0.5, anchor = "center")

        footswitch = tk.Button(pedal, text="(  )", command=self.press_footswitch)
        footswitch.place(relx=0.5, rely=0.9, anchor="s")

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

        self.value = 0

        self.midi_observer = None
        self.value_observer = None
        self.button_observer = None
        self.footswitch_observer = None

    # Display implementation
    def clear_buffer(self):
        for y in range(self.rows):
            for x in range(self.cols):
                self.buffer[y][x] = (0,0,0)
    
    def set_pixel(self, x, y, r, g, b):
        if (y < self.rows and x < self.cols):
            self.buffer[y][x] = (r,g,b)
    
    def show_buffer(self):
        self.display.delete("all")
        for y, row in enumerate(self.buffer):
            if (y > 9):
                break
            for x, pixel in enumerate(row):
                if (x > 15):
                    break
                self.display.create_rectangle(2 + scale_x * (1+x), scale_y * (1+y), scale_x * (2+x) - 4, scale_y * (2+y) - 2, fill=rgb_color(pixel))

    # Control implementation
    def observe_value(self, observer):
        self.value_observer = observer

    def set_range_and_value(self, min, val, max):
        self.min_val = min
        self.value = val
        self.max_val = max
        
    def set_value(self, value):
        self.value = value

    def observe_button(self, observer):
        self.button_observer = observer

    def observe_footswitch(self, observer):
        self.footswitch_observer = observer

    # MIDI implementation
    def observe_messages(self, observer):
        self.midi_observer = observer

    def send_message(self, message, channel=0):
        if (isinstance(message, ProgramChange)):
            self.midi_out_text.set("C{}PC{}".format(channel, message.patch))
        elif (isinstance(message, ControlChange)):
            self.midi_out_text.set("C{}CC{}V{}".format(channel, message.control, message.value))
        else:
            self.midi_out_text.set("[msg]")

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

    def change_value(self, change):
        self.value += change
        if self.value > self.max_val:
            self.value = self.min_val
        elif self.value < self.min_val:
            self.value = self.max_val
        if (self.value_observer):
            self.value_observer(self.value)

    def press_button(self):
        if (self.button_observer):
            self.button_observer()

    def press_footswitch(self):
        if (self.footswitch_observer):
            self.footswitch_observer()