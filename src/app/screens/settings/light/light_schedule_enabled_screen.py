from m5stack import lcd
from ...abstract_screen import AbstractScreen
from ...utils.string_selector import StringSelector
from app.hardware.kippenstal_config import kippenstalConfig

class LightScheduleEnabledScreen(AbstractScreen):

    def show(self):
        super().show()
        lcd.print('Light Schedule On/Off', lcd.CENTER, 85)

        lcd.setCursor(160, 125)
        value = 'On' if kippenstalConfig.isLightScheduleEnabled() else 'Off'
        self._stringSelector = StringSelector(value, 
            [ 'On', 'Off']
        )
        self._stringSelector.printToLcd()
        self._stringSelector.startEditing(self)

    def editingDone(self, editor:StringSelector):
        value = True if self._stringSelector.value == 'On' else False
        kippenstalConfig.setLightScheduleEnabled(value)
        super().back()