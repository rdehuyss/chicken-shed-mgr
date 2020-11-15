from m5stack import *
from ...abstract_screen import AbstractScreen
from ...utils.number_editor import NumberEditor
from app.hardware.kippenstal_config import kippenstalConfig
from app.hardware.kippenstal import kippenstal

class LightThresholdScreen(AbstractScreen):

    def show(self):
        super().show()
        lcd.print('Setup light threshold', lcd.CENTER, 85)

        self.numberEditor = NumberEditor(1, kippenstalConfig.getLightThreshold(), 0, 2000, '{:04d}')
        self.numberEditor.printToLcdCenter(125)
        self.numberEditor.startEditing(self)

        lcd.print('Now: {}'.format(kippenstal.currentLightSensorValue), lcd.CENTER, 165)

    def editingDone(self, editor:NumberEditor):
        kippenstalConfig.setLightThreshold(self.numberEditor.value)
        print('light threshold', self.numberEditor.value)
        super().back()

    

