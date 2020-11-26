import app.ulogging as ulogging
from machine import Timer
from .components.pca9554 import PCA9554Relay
from .kippenstal_config import kippenstalConfig

class DoorOpener:

    def __init__(self, kippenstal):
        self._kippenstal = kippenstal
        self._relayOpen = PCA9554Relay(kippenstal.i2c, kippenstalConfig.getDoorOpenerOpenRelay())
        self._relayClose = PCA9554Relay(kippenstal.i2c, kippenstalConfig.getDoorOpenerCloseRelay())
        self._isMoving = False
        self._isOpen = False
        self._hasClosedForToday = False
        self._timeDark = None
        self._timer = None


    def evaluate(self):
        if not kippenstalConfig.isDoorOpenerScheduleEnabled():
            return

        if '00' == self._kippenstal.currentHour:
            self._hasClosedForToday = False

        if self.__mustOpenDoor():
            ulogging.info('DoorOpener - Opening door')
            self.open()
            ulogging.info('DoorOpener - Door opened')
        elif self.__mustCloseDoor():
            ulogging.info('DoorOpener - Closing door')
            self.close()
            ulogging.info('DoorOpener - Door closed')
            self._timeDark = None

    def open(self):
        if self.isOpen():
            return
        self._isOpen = True
        
        self.__stopMovement()
        
        self._relayOpen.on()
        self._timer = Timer(3)
        self._timer.init(period=50000, mode=Timer.ONE_SHOT, callback=self.__stopOpen)

    def close(self):
        if self.isClosed():
            return
        
        self._hasClosedForToday = True
        self.__stopMovement()
        
        self._relayClose.on()
        self._timer = Timer(3)
        self._timer.init(period=50000, mode=Timer.ONE_SHOT, callback=self.__stopClose)

    def toggle(self):
        if self.isOpen():
            self.close()
        else:
            self.open()

    def isOpen(self):
        return self._isOpen

    def isClosed(self):
        return not self.isOpen()

    def __mustOpenDoor(self):
        if self.isOpen():
            return False

        openAtHour = int(kippenstalConfig.getDoorOpenAtHour())
        currentHour = int(self._kippenstal.currentHour)

        return openAtHour <= currentHour and not self._hasClosedForToday 

    def __mustCloseDoor(self):
        if self.isClosed():
            return False

        closeAtHour = int(kippenstalConfig.getDoorCloseAtHour())
        if self._timeDark == None:
            if self._kippenstal.currentLightSensorValue < kippenstalConfig.getLightThreshold():
                self._timeDark = self._kippenstal.currentTime
        elif self._kippenstal.currentLightSensorValue > kippenstalConfig.getLightThreshold():
            self._timeDark = None
        elif int(self._kippenstal.currentHour) > 16 and self._kippenstal.currentTime > self._timeDark + closeAtHour * (60*60):
            return True

        return False

    def __stopMovement(self):
        self._relayOpen.off()
        self._relayClose.off()
        if self._timer != None:
            self._timer.deinit()
            self._timer = None
        

    def __stopOpen(self, timer):
        self._relayOpen.off()
        self._isMoving = False
        self._timer.deinit()

    def __stopClose(self, timer):
        self._relayClose.off()
        self._isMoving = False
        self._isOpen = False
        self._timer.deinit()

    def __str__(self):
        return 'DoorOpener - Door is {}'.format('open' if self.isOpen() else 'closed')
