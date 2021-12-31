from struct import calcsize
from cores.properties import *
from cores.properties.m5 import M5
from cores.properties.tuning import Tuning
from adafruit_midi.program_change import ProgramChange
import struct

INIT = 0
VIEW = 1
EDIT = 2

class PatchCore:
    def __init__(self, root, midi, control, display):
        self.root = root
        self.midi = midi
        self.control = control
        self.display = display

        self.display.show_bitmap("patch.bin", (255,255,255))

        self.props = [M5(midi, control, display), Tuning(midi, control, display)]

        self.current_patch = None
        self.current_prop = 0
        self.last_selected_prop = 0
        self.current_mode = INIT
        
        self.midi.observe_messages(self.on_midi_message)
        self.control.observe_value(self.on_value_change)
        self.control.observe_footswitch(self.on_footswitch)
        self.control.observe_button(self.on_button)

    def on_midi_message(self, message):
        if (isinstance(message, ProgramChange)):
            self.current_patch = message.patch
            self.load_patch()
            self.to_view_mode()

    def to_view_mode(self):
        self.current_prop = self.last_selected_prop
        self.current_mode = VIEW
        for i, prop in enumerate(self.props):
            if prop.alert:
                self.current_prop = i
                break
        self.props[self.current_prop].show()
        self.control.set_range(0, len(self.props) - 1)
        self.control.set_value(self.current_prop)

    def on_value_change(self, value):
        if (self.current_mode == VIEW):
            self.last_selected_prop = value
            self.current_prop = value
            self.props[self.current_prop].show()
        elif (self.current_mode == EDIT):
            self.props[self.current_prop].update_value(value)

    def on_footswitch(self):
        if (self.current_mode == VIEW and self.props[self.current_prop].alert):
            self.props[self.current_prop].clear_alert()
            self.to_view_mode()
        elif (self.current_mode == EDIT):
            self.props[self.current_prop]

    def on_button(self, pressed):
        if (not pressed):
            return
        if (self.current_mode == VIEW):
            self.current_mode = EDIT
            self.props[self.current_prop].edit()
        elif (self.current_mode == EDIT):
            next = self.props[self.current_prop].next()
            if (not next):
                self.save_patch()
                self.to_view_mode()

    def load_patch(self):
        try:
            with open(self.patch_path(), "rb") as f:
                for prop in self.props:
                    prop.load(struct.unpack(prop.format, f.read(struct.calcsize(prop.format))))
        except OSError:
            with open(self.patch_path(), "wb") as f:
                for prop in self.props:
                    empty = bytearray(struct.calcsize(prop.format))
                    prop.load(struct.unpack(prop.format, empty))
                    f.write(empty)

    def save_patch(self):
        with open(self.patch_path(), "wb") as f:
            for prop in self.props:
                f.write(struct.pack(prop.format, *prop.save()))

    def patch_path(self):
        return "{}/storage/patches/{:03d}".format(self.root, self.current_patch)