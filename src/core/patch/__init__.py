import struct

from ports.midi_handler import MidiMessageHandler
from components.direct_menu import DirectMenu
from components.preset_menu import PresetMenu
from components.params import load_empty
from .navigator import Navigator

class PatchEditor(MidiMessageHandler):
    """
    Core for working with patches

    Responsible for loading and saving patches. Delegates all UI state to Navigator.
    """
    def __init__(self, storage_root, midi_channel, midi, control, display, direct_params, preset_params):
        self.storage_root = storage_root
        self.midi_channel = midi_channel
        self.params = preset_params

        self.menu = PresetMenu(self.params)
        self.nav = Navigator(DirectMenu(direct_params), control, display, self.save_patch)
        self.current_patch = None

        midi.register_handler(self)

    def on_program_change(self, channel, patch):
        if channel == self.midi_channel:
            self.current_patch = patch
            self.load_patch()
            self.nav.set_screen(self.menu)

    def load_patch(self):
        try:
            with open(self.patch_path(), "rb") as f:
                for param in self.params:
                    param.load(struct.unpack(param.format, f.read(struct.calcsize(param.format))))
        except (OSError, ValueError):
            with open(self.patch_path(), "wb") as f:
                for param in self.params:
                    f.write(load_empty(param))

    def save_patch(self):
        with open(self.patch_path(), "wb") as f:
            for param in self.params:
                f.write(struct.pack(param.format, *param.save()))

    def patch_path(self):
        return "{}/patches/{:03d}".format(self.storage_root, self.current_patch)
