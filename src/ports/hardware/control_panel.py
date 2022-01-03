from machine import Pin, Timer
from rotary_irq_rp2 import RotaryIRQ

class ControlPanel:
    def __init__(self, pin_btn, pin_clk, pin_dt, pin_fsw):
        self.rotary = RotaryIRQ(
            pin_clk, 
            pin_dt, 
            reverse=True, 
            range_mode=RotaryIRQ.RANGE_WRAP,
            pull_up=True,
            half_step=False)
       
        self.value_observer = self.noop
        self.button_observer = self.noop
        self.footswitch_observer = self.noop
        self.rotary.add_listener(self.__on_value_change)        
        
        self.button = DebouncedMomentarySwitch(pin_btn, self.__on_button)
        self.footswitch = DebouncedMomentarySwitch(pin_fsw, self.__on_footswitch)

    def noop(*_):
        pass

    def observe_value(self, observer):
        self.value_observer = observer
        
    def observe_button(self, observer):
        self.button_observer = observer

    def observe_footswitch(self, observer):
        self.footswitch_observer = observer

    def set_range_and_value(self, min, val, max):
        self.rotary.set(value=val,min_val=min,max_val=max)
        
    def set_value(self, value):
        self.rotary.set(value=value)

    def __on_value_change(self):
        self.value_observer(self.rotary.value())

    def __on_footswitch(self):
        self.footswitch_observer()

    def __on_button(self):
        self.button_observer()

class DebouncedMomentarySwitch:
    def __init__(self, pin, callback):
        self._pin = Pin(pin, Pin.IN, Pin.PULL_UP)
        self._pin.irq(self.__on_change, Pin.IRQ_FALLING | Pin.IRQ_RISING)
        self._timer = Timer(-1)
        self._callback = callback
        self._value = self._pin.value()

    def __on_change(self, *_):
        self._timer.init(period=20, mode=Timer.ONE_SHOT, callback=self.__after_change)

    def __after_change(self, *_):
        new_value = self._pin.value()
        if (new_value != self._value):
            self._value = new_value
            if (new_value == 0):
                self._callback()
