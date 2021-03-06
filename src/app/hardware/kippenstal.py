import utime, app.ulogging as ulogging
from machine import I2C
from .components.ds3231 import DS3231
from .light_sensor import LightSensor
from .light_control import LightControl
from .fence import Fence, FenceConstants
from .door_opener import DoorOpener
from .kippenstal_config import kippenstalConfig

class Kippenstal:

    def __init__(self):
        self.i2c = I2C(freq=400000, sda=21, scl=22)
        self.isRunning = False
        self.lightSensor = LightSensor(self)
        self.light = LightControl(self)
        self.fence = Fence(self)
        self.doorOpener = DoorOpener(self)
        self.timeDark = None
        self.ds3231 = DS3231(self.i2c)
        self.ds3231.get_time(set_rtc=True)
        self.start()

    def start(self):
        self.isRunning = True
        ulogging.info('Kippenstal Mgr started')

    def stop(self):
        self.isRunning = False
        ulogging.info('Kippenstal Mgr stopped')

    def getTemperature(self):
        return self.ds3231.get_temperature()

    def evaluate(self):
        if self.isRunning:
            self.currentTime = utime.time()
            self.currentHour = "{}".format(utime.strftime('%H', utime.localtime()))
            self.currentHourMinute = "{}".format(utime.strftime('%H:%M', utime.localtime()))
            self.currentLightSensorValue = self.lightSensor.luminance()
            self.isLight = self.__isItLight()
            self.isDark = not self.isLight

            self.light.evaluate()
            self.doorOpener.evaluate()
            self.fence.evaluate()

    def __isItLight(self):
        isLight = self.currentLightSensorValue >= kippenstalConfig.getLightThreshold()
        if isLight:
            self.timeDark = None
        elif self.timeDark == None:
            self.timeDark = self.currentTime
        return isLight

    def saveTime(self):
        self.ds3231.save_time()

kippenstal = Kippenstal()