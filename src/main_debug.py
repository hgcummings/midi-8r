"""
Debug boot script for running on Raspberry Pi Pico

Useful for developing/debugging custom core

Uses real hardware ports for the display and control panel, with shell-emulated MIDI
"""

from core.patch import PatchEditor
from ports.emulated.shell_midi import ShellMidi
from ports.hardware.rgb_matrix import RgbMatrix
from ports.hardware.control_panel import ControlPanel
from adapters.display import Display

from config import *

midi = ShellMidi()
display = Display(RgbMatrix(RGB_MATRIX_PIN_DT, RGB_MATRIX_ROWS, RGB_MATRIX_COLS, dim_factor=16))

core = PatchEditor(
    "/storage",
    MIDI_CHANNEL_IN,
    midi,
    ControlPanel(ENCODER_PIN_BTN, ENCODER_PIN_CLK, ENCODER_PIN_DT, FOOTSWITCH_PIN),
    display,
    init_components(midi)
)
