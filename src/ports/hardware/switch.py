from machine import Pin, Timer

class DebouncedMomentarySwitch:
    def __init__(self, pin, down_callback, up_callback=None):
        self._pin = Pin(pin, Pin.IN, Pin.PULL_UP)
        self._pin.irq(self.__on_change, Pin.IRQ_FALLING | Pin.IRQ_RISING)
        self._timer = Timer(-1)
        self._down_callback = down_callback
        self._up_callback = up_callback
        self._value = self._pin.value()

    def __on_change(self, *_):
        self._timer.init(period=20, mode=Timer.ONE_SHOT, callback=self.__after_change)

    def __after_change(self, *_):
        new_value = self._pin.value()
        if (new_value != self._value):
            self._value = new_value
            if (new_value == 0):
                self._callback()
            else if (self._up_callback):
                self._up_callback()
