import tkinter as tk
from tkinter.constants import DISABLED
from adafruit_midi.program_change import ProgramChange
from adapters.control import EncoderEvent
from functools import partial

# Pedal dimensions in mm: 70x110
# Pedal dimensions in px: 308x484
# Pixels per mm: 4.4

# Display dimensions
width = 16
height = 10
scale_x = 15
scale_y = 10

def rgb_color(rgb):
    return "#%02x%02x%02x" % rgb  

class Application:
    def __init__(self):
        self.app = tk.Tk()

        pedal = tk.Frame(self.app, width=308, height=484, background="black")
        pedal.grid(column=0, columnspan=3, row=0)

        self.display = tk.Canvas(pedal, width=scale_x*(width+2), height=scale_y*(height+2), background="black")
        self.display.place(relx = 0.5, rely = 0.1, anchor = "n")

        encoder_frame = tk.Frame(pedal)
        encoder_decr = tk.Button(encoder_frame, text="<", command=partial(self.send_encoder_event, EncoderEvent.DECREMENT))
        encoder_decr.grid(column=0, row=0)
        encoder = tk.Button(encoder_frame, text="O")
        encoder.bind("<Button-1>", partial(self.send_encoder_event, EncoderEvent.PUSH))
        encoder.bind("<ButtonRelease-1>", partial(self.send_encoder_event, EncoderEvent.RELEASE))
        encoder.grid(column=1, row=0)
        encoder_decr = tk.Button(encoder_frame, text=">", command=partial(self.send_encoder_event, EncoderEvent.INCREMENT))
        encoder_decr.grid(column=2, row=0)
        encoder_frame.place(relx = 0.5, rely = 0.5, anchor = "center")

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
        self.encoder_observer = None

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

    # Control implementation
    def observe_encoder(self, observer):
        self.encoder_observer = observer

    # MIDI implementation
    def observe_messages(self, observer):
        self.midi_observer = observer

    def send_message(self, message):
        if (isinstance(message, ProgramChange)):
            self.midi_out_text.set("P" + str(message.patch))
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

    def send_encoder_event(self, event, _=None):
        if (self.encoder_observer):
            self.encoder_observer(event)