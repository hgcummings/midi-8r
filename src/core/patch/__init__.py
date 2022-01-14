import struct

from ports.midi_handler import MidiMessageHandler
from .boot_screen import BootScreen
from .property_menu import PropertyMenu
from .ui_state_manager import UiStateManager

class PatchEditor(MidiMessageHandler):
    """
    Core for working with patches

    Responsible for loading and saving patches. All other mutable state is
    controlled via the `ui_state_manager.UiStateManager`

    Delegates to `components` for showing or editing parameters,
    passing through events from the control panel to enable this
    """
    def __init__(self, storage_root, midi_channel, midi, control, display, properties):
        self.storage_root = storage_root
        self.midi_channel = midi_channel

        self.props = properties

        self.menu = PropertyMenu(self.props)
        self.state = UiStateManager(BootScreen(), control, display)
        self.current_patch = None
        
        midi.register_handler(self)
        control.observe_value(self.on_value_change)
        control.observe_footswitch(self.on_footswitch)
        control.observe_button(self.on_button)

    def on_program_change(self, channel, patch):
        if channel == self.midi_channel:
            self.current_patch = patch
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
