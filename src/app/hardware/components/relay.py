import machine

class PinRelay:

    def __init__(self, pin):
        self._pin = machine.Pin(pin, machine.Pin.OUT)
        self.off()

    def on(self):
        self._pin.value(1)
        self.value = True

    def off(self):
        self._pin.value(0)
        self.value = False

    def toggle(self):
        if self.isOn():
            self.off()
        else:
            self.on()

    def isOn(self):
        return self.value

    def isOff(self):
        return not self.isOn()

    def __str__(self):
        return "pin " + str(self._pin) + " = " + str(self.value) + " (" + str(self._pin.value()) + ")"