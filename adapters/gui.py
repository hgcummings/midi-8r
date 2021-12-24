import tkinter as tk


class Application:
    def __init__(self):
        self.app = tk.Tk()

        self.display = tk.Label(self.app)
        self.display.grid(column = 0, columnspan=2, row=0)

        self.midi_in = tk.Entry(self.app)
        self.midi_in.grid(column = 1, row = 1)

        midi_in_send = tk.Button(self.app, text="Send", command=self.send_midi_in)
        midi_in_send.grid(column = 1, row = 2)

        self.prog_change_observer = None

    def show_ui(self):
        self.app.mainloop()

    def observe_prog_change(self, observer):
        self.prog_change_observer = observer

    def show_preset(self, value):
        self.display.configure(text = "P" + str(value))

    def send_midi_in(self):
        if (self.prog_change_observer):
            self.prog_change_observer(int(self.midi_in.get()))