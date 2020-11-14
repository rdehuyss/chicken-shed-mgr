from m5stack import *
from ...abstract_screen import AbstractScreen
from ...utils.number_editor import NumberEditor
from main.hardware.kippenstal_config import kippenstalConfig

class LightFromToHourScreen(AbstractScreen):

    def show(self):
        super().show()
        lcd.print('Setup light threshold', lcd.CENTER, 85)

        self.fromHourEditor = NumberEditor(1, kippenstalConfig.getLightFromHour(), 0, 23, '{:02d}', 'h')
        self.toHourEditor = NumberEditor(2, kippenstalConfig.getLightToHour(), 0, 23, '{:02d}', 'h')

        lcd.setCursor(98, 125)
        self.fromHourEditor.printToLcd()
        lcd.print(' - ')
        self.toHourEditor.printToLcd()
        self.fromHourEditor.startEditing(self)


    def editingDone(self, numberEditor:NumberEditor):
        if numberEditor.nbr == 1:
            kippenstalConfig.setLightFromHour(self.fromHourEditor.value)
            self.toHourEditor.startEditing(self)
        elif numberEditor.nbr == 2:
            kippenstalConfig.setLightToHour(self.toHourEditor.value)
            super().back()
