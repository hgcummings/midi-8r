from rotary_irq_rp2 import RotaryIRQ
from machine import Pin

class Encoder:
    def __init__(self, pin_btn, pin_clk, pin_dt, max_val):
        self.rotary = RotaryIRQ(
            pin_clk, 
            pin_dt, 
            min_val=0, 
            max_val=max_val, 
            reverse=True, 
            range_mode=RotaryIRQ.RANGE_WRAP,
            pull_up=True,
            half_step=False)
       
        self.value_observer = None
        self.button_observer = None
        self.rotary.add_listener(self.on_value_change)        
        
        self.button_pin = Pin(pin_btn, Pin.IN, Pin.PULL_UP)
        self.button_pin.irq(self.on_button_change, Pin.IRQ_FALLING | Pin.IRQ_RISING)

    def observe_value(self, observer):
        self.value_observer = observer
        
    def observe_buttons(self, observer):
        self.button_observer = observer
        
    def set_value(self, value):
        self.rotary.set(value=value)

    def on_value_change(self):
        if (self.value_observer):
            self.value_observer(self.rotary.value())
        
    def on_button_change(self, pressed):
        print(self.button_pin.value())
        if (self.button_observer):
            self.button_observer(not self.button_pin.value())