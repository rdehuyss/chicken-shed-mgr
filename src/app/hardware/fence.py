import app.ulogging as ulogging
from .components.pca9554 import PCA9554Relay
from .kippenstal_config import kippenstalConfig

class FenceConstants:
    alwaysOn = "on"
    onWhenDoorOpen = "on when door open"
    alwaysOff = "off"

class Fence(PCA9554Relay):

    def __init__(self, kippenstal):
        super().__init__(kippenstal.i2c, kippenstalConfig.getFenceRelay())
        self._kippenstal = kippenstal

    def evaluate(self):
        if self.__mustTurnOnFence():
            self.on()
            ulogging.info('Fence - electrified')
        elif self.__mustTurnOffFence():
            self.off()
            ulogging.info('Fence - not electrified')

    def __mustTurnOnFence(self):
        if self.isOn() or kippenstalConfig.getFenceOnState() == FenceConstants.alwaysOff:
            return False

        if kippenstalConfig.getFenceOnState() == FenceConstants.alwaysOn:
            return True
        elif kippenstalConfig.getFenceOnState() == FenceConstants.onWhenDoorOpen and self._kippenstal.doorOpener.isOpen():
            return True

        return False

    def __mustTurnOffFence(self):
        if self.isOff() or kippenstalConfig.getFenceOnState() == FenceConstants.alwaysOn:
            return False

        if kippenstalConfig.getFenceOnState() == FenceConstants.alwaysOff:
            return True
        elif kippenstalConfig.getFenceOnState() == FenceConstants.onWhenDoorOpen and self._kippenstal.doorOpener.isClosed():
            return True

        return False
