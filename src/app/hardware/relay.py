import machine

class Relay:

    def __init__(self, pin):
        self.pin = machine.Pin(pin, machine.Pin.OUT)
        self.off()

    def on(self):
        self.pin.value(1)
        self.value = True
        print('\t', str(self))

    def off(self):
        self.pin.value(0)
        self.value = False
        print('\t', str(self))

    def isOn(self):
        return self.value

    def isOff(self):
        return not self.isOn()

    def __str__(self):
        return "pin " + str(self.pin) + " = " + str(self.value) + " (" + str(self.pin.value()) + ")"