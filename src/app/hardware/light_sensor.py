"""
Micropython BH1750 ambient light sensor driver.
"""
import machine, utime
from .sensors.bh1750 import BH1750


class LightSensor():
    
    def __init__(self, updateRate:int = 60):
        i2c = machine.I2C(freq=400000, sda=21, scl=22)
        self.bh1750 = BH1750(i2c)
        self.updateRate = updateRate
        self.lastLightSensorMeasurementTime = 0
        self.currentLightSensorValue = -1

    def luminance(self):
        currentTime = utime.time()
        if self.currentLightSensorValue < 0 or int(currentTime) > int(self.lastLightSensorMeasurementTime + self.updateRate):
            self.currentLightSensorValue = self.getLuminanceFromSensor()
            self.lastLightSensorMeasurementTime = currentTime
        
        return self.currentLightSensorValue

    def getLuminanceFromSensor(self):
        try:
            return int(self.bh1750.luminance(BH1750.ONCE_HIRES_1))        
        except:
            try: 
                return int(self.bh1750.luminance(BH1750.ONCE_HIRES_1))
            except:
                return -1

    def __str__(self):
        return 'LightSensor - {} lux'.format(self.currentLightSensorValue)
        