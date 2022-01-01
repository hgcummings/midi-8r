from cores.properties import *
from cores.properties.m5 import M5
from cores.properties.tuning import Tuning
from adafruit_midi.program_change import ProgramChange
import struct

class PropertyMenu:
    def __init__(self, props):
        self.props = props
        self.current_prop = 0
        self.last_selected_prop = 0

    def __show_edit(self, display):
        self.current_prop = self.last_selected_prop
        for i, prop in enumerate(self.props):
            if prop.alert:
                self.current_prop = i
                break
        self.props[self.current_prop].show_view(display)

    def switch(self, display):
        if (self.props[self.current_prop].alert):
            self.props[self.current_prop].clear_alert()
            self.__show_edit(display)

    def edit(self, display):
        self.__show_edit(display)
        return (0, self.current_prop, len(self.props) - 1)

    def update_value(self, value, display):
        self.last_selected_prop = value
        self.current_prop = value
        self.props[self.current_prop].show_view(display)

    def next(self):
        return self.props[self.current_prop]

class BootScreen:
    def edit(self, display):
        display.show_bitmap("patch.bin", (255,255,255))
        return (0,0,0)

    def update_value(self, *_):
        pass

    def switch(self, *_):
        pass

    def next(self):
        return self

class UiStateManager:
    def __init__(self, editor, control, display):
        # External state-holding objects
        self.__control = control
        self.__display = display

        # Internal state
        self.set_editor(editor)

    def set_editor(self, editor):
        self.__editor = editor
        self.__control.set_range_and_value(*self.__editor.edit(self.__display))

    def edit(self):
        return self.__editor.edit(self.__display)

    def update_value(self, value):
        self.__editor.update_value(value, self.__display)

    def switch(self):
        self.__editor.switch(self.__display)

    def next(self):
        return self.__editor.next()

class PatchCore:
    def __init__(self, storage_root, midi, control, display):
        self.root = storage_root

        self.props = [M5(midi), Tuning(midi)]

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
            self.state.set_editor(self.menu)

    def on_value_change(self, value):
        self.state.update_value(value)

    def on_footswitch(self):
        self.state.switch()

    def on_button(self, pressed):
        if (not pressed):
            return

        next_state = self.state.next()
        if (next_state == None):
            # We've exited a property editor, so need to save any changes
            self.save_patch()
            next_state = self.menu

        self.state.set_editor(next_state)

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
