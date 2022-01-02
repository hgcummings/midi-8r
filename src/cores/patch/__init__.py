from .components.boot_screen import BootScreen
from .components.property_menu import PropertyMenu
from .components.m5 import M5
from .components.tuning import Tuning
from .components.guitar import Guitar
from .ui_state_manager import UiStateManager

from adafruit_midi.program_change import ProgramChange
import struct

class PatchCore:
    def __init__(self, storage_root, midi, control, display):
        self.storage_root = storage_root

        self.props = [M5(midi.send_message), Tuning(midi.send_message), Guitar()]

        self.menu = PropertyMenu(self.props)
        self.state = UiStateManager(BootScreen(), control, display)
        self.current_patch = None
        
        midi.observe_messages(self.on_midi_message)
        control.observe_value(self.on_value_change)
        control.observe_footswitch(self.on_footswitch)
        control.observe_button(self.on_button)

    def on_midi_message(self, message):
        if (isinstance(message, ProgramChange)):
            self.current_patch = message.patch
            self.load_patch()
            self.state.set_component(self.menu)

    def on_value_change(self, value):
        self.state.update_value(value)

    def on_footswitch(self):
        self.state.switch()

    def on_button(self):
        next_state = self.state.next()
        if (next_state == None):
            # We've exited a property editor, so need to save any changes
            self.save_patch()
            next_state = self.menu

        self.state.set_component(next_state)

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
        return "{}/patches/{:03d}".format(self.storage_root, self.current_patch)
