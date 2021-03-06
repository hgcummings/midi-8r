from rotary_irq_rp2 import RotaryIRQ
from .switch import DebouncedMomentarySwitch

class ControlPanel:
    """Hardware control panel consisting of a rotary encoder (with push button) and footswitch"""
    def __init__(self, pin_btn, pin_clk, pin_dt, pin_fsw):
        self.rotary = RotaryIRQ(
            pin_clk, 
            pin_dt, 
            reverse=True, 
            range_mode=RotaryIRQ.RANGE_WRAP,
            pull_up=True,
            half_step=False)
       
        self.value_observer = self.__noop
        self.button_observer = self.__noop
        self.footswitch_observer = self.__noop
        self.rotary.add_listener(self.__on_value_change)        
        
        self.button = DebouncedMomentarySwitch(pin_btn, self.__on_button)
        self.footswitch = DebouncedMomentarySwitch(pin_fsw, self.__on_footswitch)

    def set_range_and_value(self, min, val, max):
        """Set the minimum allowed, current, and maximum allowed value for the rotary encoder"""
        self.rotary.set(value=val,min_val=min,max_val=max)
        
    def set_value(self, value):
        """Set the current value for the rotary encoder"""
        self.rotary.set(value=value)

    def observe_value(self, observer):
        self.value_observer = observer
        
    def observe_button(self, observer):
        self.button_observer = observer

    def observe_footswitch(self, observer):
        self.footswitch_observer = observer

    def __on_value_change(self):
        self.value_observer(self.rotary.value())

    def __on_button(self):
        self.button_observer()

    def __on_footswitch(self):
        self.footswitch_observer()

    def __noop(*_):
        pass
