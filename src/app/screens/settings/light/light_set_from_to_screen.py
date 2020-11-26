from m5stack import lcd
from ...abstract_screen import AbstractScreen
from ...utils.number_editor import NumberEditor
from app.hardware.kippenstal_config import kippenstalConfig

class LightFromToHourScreen(AbstractScreen):

    def show(self):
        super().show()
        lcd.print('Setup light threshold', lcd.CENTER, 85)

        self._fromHourEditor = NumberEditor(1, kippenstalConfig.getLightFromHour(), 0, 23, '{:02d}', 'h')
        self._toHourEditor = NumberEditor(2, kippenstalConfig.getLightToHour(), 0, 23, '{:02d}', 'h')

        lcd.setCursor(98, 125)
        self._fromHourEditor.printToLcd()
        lcd.print(' - ')
        self._toHourEditor.printToLcd()
        self._fromHourEditor.startEditing(self)


    def editingDone(self, numberEditor:NumberEditor):
        if numberEditor.nbr == 1:
            kippenstalConfig.setLightFromHour(self._fromHourEditor.value)
            self._toHourEditor.startEditing(self)
        elif numberEditor.nbr == 2:
            kippenstalConfig.setLightToHour(self._toHourEditor.value)
            super().back()
