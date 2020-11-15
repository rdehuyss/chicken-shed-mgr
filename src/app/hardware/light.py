import app.ulogging as ulogging
from .relay import Relay
from .kippenstal_config import kippenstalConfig

class Light(Relay):

    def __init__(self, kippenstal):
        super().__init__(kippenstalConfig.getLightRelay())
        self.kippenstal = kippenstal
        self.toggleTime = 0

    def evaluate(self):
        if not kippenstalConfig.isLightScheduleEnabled() or self.kippenstal.currentTime < (self.toggleTime + 3600):
            return

        if self.__mustTurnOnLight():
            self.on()
            ulogging.info('Light - on')
        elif self.__mustTurnOffLight():
            self.off()
            ulogging.info('Light - off')

    def toggle(self):
        super().toggle()
        self.toggleTime = self.kippenstal.currentTime

    def __mustTurnOnLight(self):
        if self.isOn():
            return False

        if self.__isInsideLightTimeRange() and self.__isDark():
            return True

        return False

    def __mustTurnOffLight(self):
        if self.isOff():
            return False

        if self.__isLight() or self.__isOutsideLightTimeRange():
            return True

        return False

    def __isInsideLightTimeRange(self):
        current_hour = int(self.kippenstal.currentHour)
        if kippenstalConfig.getLightFromHour() <= current_hour and current_hour < kippenstalConfig.getLightToHour():
                return True
        
        return False

    def __isOutsideLightTimeRange(self):
        return not self.__isInsideLightTimeRange()

    def __isLight(self):
        lightSensorValue = self.kippenstal.currentLightSensorValue
        lightSensorThreshold = kippenstalConfig.getLightThreshold()
        return lightSensorValue >= lightSensorThreshold

    def __isDark(self):
        return not self.__isLight()

    def __str__(self):
        return 'Light - Light is {}'.format('on' if self.isOn() else 'off')