from m5stack import *
from ...abstract_screen import AbstractScreen
from ...utils.string_selector import StringSelector
from app.hardware.kippenstal_config import kippenstalConfig
from app.hardware.fence import FenceConstants

class FenceStateSelectorScreen(AbstractScreen):

    def show(self):
        super().show()
        lcd.print('Setup Fence On/Off', lcd.CENTER, 85)

        lcd.setCursor(160, 125)
        self.stringSelector = StringSelector(kippenstalConfig.getFenceOnState(), 
            [ FenceConstants.alwaysOn, FenceConstants.onWhenDoorOpen, FenceConstants.alwaysOff]
        )
        self.stringSelector.printToLcd()
        self.stringSelector.startEditing(self)

    def editingDone(self, editor:StringSelector):
        print('Fence state', self.stringSelector.value)
        kippenstalConfig.setFenceOnState(self.stringSelector.value)
        super().back()

    

