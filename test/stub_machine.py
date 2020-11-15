from test.stub_module import StubModule, MockCallable

known_pins = []

class PinStub:
    OUT = 2

    def __init__(self, pin, dir):
        self.pin = pin
        self.dir = dir
        self.is_not_init = True
        self.vals = [-1]
        global known_pins
        known_pins.append(self)

    def value(self, val = -1):
        if self.is_not_init:
            self.is_not_init = False
            return self.lastVal()

        if val != -1:
            self.vals.append(val)
        return self.lastVal()

    def lastVal(self):
        return self.vals[-1]

    def __str__(self):
        return "StubPin {} - {}".format(str(self.pin), "high" if self.lastVal() == 1 else "low") 

class TimerStub:
    ONE_SHOT = 2

    def __init__(self, nbr):
        self.nbr = nbr

    def init(self, freq=100, prescaler=2, period=None, mode=None, callback=None):
        pass

    def deinit(self):
        pass

    



machine = StubModule('machine')
machine.Pin = PinStub
machine.Timer = TimerStub