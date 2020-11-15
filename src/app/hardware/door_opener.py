import utime, app.ulogging as ulogging
from machine import Timer
from .relay import Relay
from .kippenstal_config import kippenstalConfig

class DoorOpener:

    def __init__(self, kippenstal):
        self.kippenstal = kippenstal
        self._relayOpen = Relay(kippenstalConfig.getDoorOpenerOpenRelay())
        self._relayClose = Relay(kippenstalConfig.getDoorOpenerCloseRelay())
        self._isMoving = False
        self._isOpen = False
        self._hasClosedForToday = False
        self._timeDark = None
        self.timer = None


    def evaluate(self):
        if not kippenstalConfig.isDoorOpenerScheduleEnabled():
            return

        if '00' == self.kippenstal.currentHour:
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
        self.timer = Timer(3)
        self.timer.init(period=50000, mode=Timer.ONE_SHOT, callback=self.__stopOpen)

    def close(self):
        if self.isClosed():
            return
        
        self._hasClosedForToday = True
        self.__stopMovement()
        
        self._relayClose.on()
        self.timer = Timer(3)
        self.timer.init(period=50000, mode=Timer.ONE_SHOT, callback=self.__stopClose)

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
        currentHour = int(self.kippenstal.currentHour)

        return openAtHour <= currentHour and not self._hasClosedForToday 

    def __mustCloseDoor(self):
        if self.isClosed():
            return False

        closeAtHour = int(kippenstalConfig.getDoorCloseAtHour())
        if self._timeDark == None:
            if self.kippenstal.currentLightSensorValue < 10:
                self._timeDark = utime.time()
        elif utime.time() > self._timeDark + closeAtHour * (60*60):
            return True

        return False

    def __stopMovement(self):
        self._relayOpen.off()
        self._relayClose.off()
        if self.timer != None:
            self.timer.deinit()
            self.timer = None
        

    def __stopOpen(self, timer):
        self._relayOpen.off()
        self._isMoving = False
        self.timer.deinit()

    def __stopClose(self, timer):
        self._relayClose.off()
        self._isMoving = False
        self._isOpen = False
        self.timer.deinit()

    def __str__(self):
        return 'DoorOpener - Door is {}'.format('open' if self.isOpen() else 'closed')
