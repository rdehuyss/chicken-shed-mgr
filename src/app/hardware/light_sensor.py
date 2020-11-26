"""
Micropython BH1750 ambient light sensor driver.
"""
import machine, utime
from .components.bh1750 import BH1750


class LightSensor():
    
    def __init__(self, kippenstal, updateRate:int = 60):
        try:
            self._bh1750 = BH1750(kippenstal.i2c)
            self._updateRate = updateRate
            self._lastLightSensorMeasurementTime = 0
        except OSError:
            self._bh1750 = None
        self._currentLightSensorValue = -1

    def luminance(self):
        currentTime = utime.time()
        if self._currentLightSensorValue < 0 or int(currentTime) > int(self._lastLightSensorMeasurementTime + self._updateRate):
            self._currentLightSensorValue = self.getLuminanceFromSensor()
            self._lastLightSensorMeasurementTime = currentTime
        
        return self._currentLightSensorValue

    def getLuminanceFromSensor(self):
        if self._bh1750 is None:
            return -1
            
        try:
            return int(self._bh1750.luminance(BH1750.ONCE_HIRES_1))        
        except:
            try: 
                return int(self._bh1750.luminance(BH1750.ONCE_HIRES_1))
            except:
                return -1

    def __str__(self):
        return 'LightSensor - {} lux'.format(self._currentLightSensorValue)
        