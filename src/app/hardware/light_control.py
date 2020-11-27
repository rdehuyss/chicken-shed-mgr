import app.ulogging as ulogging
from .components.pca9554 import PCA9554Relay
from .kippenstal_config import kippenstalConfig

class LightControl:

    def __init__(self, kippenstal):
        self._light1 = PCA9554Relay(kippenstal.i2c, kippenstalConfig.getLight1Relay())
        self._light2 = PCA9554Relay(kippenstal.i2c, kippenstalConfig.getLight2Relay())
        self._kippenstal = kippenstal
        self._toggleTime = 0

    def evaluate(self):
        if not kippenstalConfig.isLightScheduleEnabled() or self._kippenstal.currentTime < (self._toggleTime + 900):
            return

        self.__evaluateLight('Light 1', self._light1, kippenstalConfig.getLight1From(), kippenstalConfig.getLight1To())
        self.__evaluateLight('Light 2', self._light2, kippenstalConfig.getLight2From(), kippenstalConfig.getLight2To())

    def toggle(self):
        self._toggleTime = self._kippenstal.currentTime
        if self._light1.isOff():
            self._light1.on()
            self._light2.on()
            ulogging.info('LightControl - Lights Toggled Manually - Light 1 & 2 - on')
        else:
            self._light1.off()
            self._light2.off()
            ulogging.info('LightControl - Lights Toggled Manually - Light 1 & 2 - off')

    def __evaluateLight(self, name:str, light:PCA9554Relay, fromTime:str, toTime:str):
        if self.__mustTurnOnLight(light, fromTime, toTime):
            light.on()
            ulogging.info('LightControl - {} - on'.format(name))
        elif self.__mustTurnOffLight(light, fromTime, toTime):
            light.off()
            ulogging.info('LightControl - {} - off'.format(name))

    def __mustTurnOnLight(self, light:PCA9554Relay, fromTime:str, toTime:str):
        if light.isOn():
            return False

        if self.__isInsideTimeRange(fromTime, toTime) and self._kippenstal.isDark:
            return True

        return False

    def __mustTurnOffLight(self, light:PCA9554Relay, fromTime:str, toTime:str):
        if light.isOff():
            return False

        if self._kippenstal.isLight or self.__isOutsideTimeRange(fromTime, toTime):
            return True

        return False

    def __isInsideTimeRange(self, fromTime:str, toTime:str):
        if fromTime <= self._kippenstal.currentHourMinute and self._kippenstal.currentHourMinute < toTime:
                return True
        
        return False

    def __isOutsideTimeRange(self, fromTime:str, toTime:str):
        return not self.__isInsideTimeRange(fromTime, toTime)