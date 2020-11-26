from m5stack import lcd
from ...abstract_screen import AbstractScreen
from ...utils.string_selector import StringSelector
from app.hardware.kippenstal_config import kippenstalConfig
from app.hardware.fence import FenceConstants

class FenceStateSelectorScreen(AbstractScreen):

    def show(self):
        super().show()
        lcd.print('Setup Fence On/Off', lcd.CENTER, 85)

        lcd.setCursor(160, 125)
        self._stringSelector = StringSelector(kippenstalConfig.getFenceOnState(), 
            [ FenceConstants.alwaysOn, FenceConstants.onWhenDoorOpen, FenceConstants.alwaysOff]
        )
        self._stringSelector.printToLcd()
        self._stringSelector.startEditing(self)

    def editingDone(self, editor:StringSelector):
        kippenstalConfig.setFenceOnState(self._stringSelector.value)
        super().back()

    

