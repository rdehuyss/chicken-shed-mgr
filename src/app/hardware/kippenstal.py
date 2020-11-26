import utime, app.ulogging as ulogging
from machine import Timer, I2C
from .light_sensor import LightSensor
from .light import Light
from .fence import Fence, FenceConstants
from .door_opener import DoorOpener

class Kippenstal:

    def __init__(self):
        self.i2c = I2C(freq=400000, sda=21, scl=22)
        self.lightSensor = LightSensor(self)
        self.light = Light(self)
        self.fence = Fence(self)
        self.doorOpener = DoorOpener(self)
        self.start()

    def start(self):
        self.__watcher(None)
        self._timer = Timer(2)
        self._timer.init(period=60000, mode=Timer.PERIODIC, callback=self.__watcher)
        ulogging.info('Kippenstal Mgr started')

    def stop(self):
        self._timer.deinit()
        ulogging.info('Kippenstal Mgr stopped')

    def status(self):
        door_status = '\n\t- ' + str(self.doorOpener)
        fence_status = '\n\t- ' + str(self.fence)
        light_status = '\n\t- ' + str(self.light)
        light_sensor_status = '\n\t- ' + str(self.lightSensor)
        ulogging.info('Kippenstal status' + door_status + fence_status + light_status + light_sensor_status)

    def __watcher(self, timer):
        self.currentTime = utime.time()
        self.currentHour = "{}".format(utime.strftime('%H', utime.localtime()))
        self.currentLightSensorValue = self.lightSensor.luminance()

        self.light.evaluate()
        self.doorOpener.evaluate()
        self.fence.evaluate()


kippenstal = Kippenstal()