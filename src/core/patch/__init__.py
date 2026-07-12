import struct

from ports.midi_handler import MidiMessageHandler
from components.direct_menu import DirectMenu
from components.preset_menu import PresetMenu
from .navigator import Navigator

class PatchEditor(MidiMessageHandler):
    """
    Core for working with patches

    Responsible for loading and saving patches. Delegates all UI state to Navigator.
    """
    def __init__(self, storage_root, midi_channel, midi, control, display, direct_props, preset_props):
        self.storage_root = storage_root
        self.midi_channel = midi_channel
        self.props = preset_props

        self.menu = PresetMenu(self.props)
        self.nav = Navigator(DirectMenu(direct_props), control, display, self.save_patch)
        self.current_patch = None

        midi.register_handler(self)

    def on_program_change(self, channel, patch):
        if channel == self.midi_channel:
            self.current_patch = patch
            self.load_patch()
            self.nav.set_component(self.menu)

    def load_patch(self):
        try:
            with open(self.patch_path(), "rb") as f:
                for prop in self.props:
                    prop.load(struct.unpack(prop.format, f.read(struct.calcsize(prop.format))))
        except (OSError, ValueError):
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
