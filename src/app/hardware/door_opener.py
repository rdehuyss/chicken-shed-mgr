import app.ulogging as ulogging
from machine import Timer
from .components.pca9554 import PCA9554Relay
from .kippenstal_config import kippenstalConfig

class DoorOpener:

    def __init__(self, kippenstal):
        self._kippenstal = kippenstal
        self._relayOpen = PCA9554Relay(kippenstal.i2c, kippenstalConfig.getDoorOpenerOpenRelay())
        self._relayClose = PCA9554Relay(kippenstal.i2c, kippenstalConfig.getDoorOpenerCloseRelay())
        self._isOpen = False
        self._hasClosedForToday = False
        self._timer = None


    def evaluate(self):
        if not kippenstalConfig.isDoorOpenerScheduleEnabled():
            return

        if '00' == self._kippenstal.currentHour:
            self._hasClosedForToday = False

        if self.__mustOpenDoor():
            self.open()
        elif self.__mustCloseDoor():
            self.close()

    def open(self):
        if self.isOpen():
            return
        ulogging.info('DoorOpener - Opening door')
        self._isOpen = True
        
        self.__stopMovement()
        
        self._relayOpen.on()
        self._timer = Timer(3)
        self._timer.init(period=50000, mode=Timer.ONE_SHOT, callback=self.__stopOpen)

    def close(self):
        if self.isClosed():
            return
        ulogging.info('DoorOpener - Closing door')

        self.__stopMovement()

        self._hasClosedForToday = True
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
        return not self._isOpen

    def __mustOpenDoor(self):
        if self.isOpen():
            return False

        openAtHour = int(kippenstalConfig.getDoorOpenAtHour())
        currentHour = int(self._kippenstal.currentHour)

        return openAtHour <= currentHour and self._kippenstal.isLight and not self._hasClosedForToday 

    def __mustCloseDoor(self):
        if self.isClosed():
            return False

        closeAtHour = int(kippenstalConfig.getDoorCloseAtHour())
        if int(self._kippenstal.currentHour) > 16 and self._kippenstal.isDark and self._kippenstal.currentTime > self._kippenstal.timeDark + closeAtHour * (60*60):
            return True
            
        return False

    def __stopMovement(self):
        self._relayOpen.off()
        self._relayClose.off()
        if self._timer != None:
            self._timer.deinit()
            self._timer = None

    def __stopOpen(self, timer):
        self.__stopMovement()
        ulogging.info('DoorOpener - Door opened')

    def __stopClose(self, timer):
        self.__stopMovement()
        self._isOpen = False
        ulogging.info('DoorOpener - Door closed')

    def __str__(self):
        return 'DoorOpener - Door is {}'.format('open' if self.isOpen() else 'closed')
