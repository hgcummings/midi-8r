from rotary_irq_rp2 import RotaryIRQ

class Encoder:
    def __init__(self, pin_a, pin_b, max_val):
        self.rotary = RotaryIRQ(
            pin_a, 
            pin_b, 
            min_val=0, 
            max_val=max_val, 
            reverse=True, 
            range_mode=RotaryIRQ.RANGE_WRAP,
            pull_up=True,
            half_step=False)
       
        self.rotary.add_listener(self.on_value_change)
        self.value_observer = None
        self.button_observer = None
        
    def observe_value(self, observer):
        self.value_observer = observer
        
    def observe_buttons(self, observer):
        self.button_observer = observer
        
    def on_value_change(self):
        print(self.rotary.value())
        if (self.value_observer):
            self.value_observer(self.rotary.value())
        
    def set_value(self, value):
        self.rotary.set(value=value)
