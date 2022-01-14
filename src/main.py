"""
Primary boot script for running on Raspberry Pi Pico

Uses real hardware ports (display, control panel, MIDI) with a fully-featured core
"""

from core.patch import PatchEditor
from ports.hardware.midi_uart import MidiOverUart
from ports.hardware.control_panel import ControlPanel
from ports.hardware.rgb_matrix import RgbMatrix
from adapters.midi_thru import MidiThru
from adapters.display import Display
from config import *

midi = MidiThru(MidiOverUart(MIDI_UART_PIN_TX, MIDI_UART_PIN_RX, MIDI_CHANNEL_IN, MIDI_CHANNEL_OUT))

core = PatchEditor(
    "/storage",
    midi,
    ControlPanel(ENCODER_PIN_BTN, ENCODER_PIN_CLK, ENCODER_PIN_DT, FOOTSWITCH_PIN),
    Display(RgbMatrix(RGB_MATRIX_PIN_DT, RGB_MATRIX_ROWS, RGB_MATRIX_COLS)),
    init_components(midi)
)
