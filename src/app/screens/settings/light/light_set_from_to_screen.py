from m5stack import lcd
from ...abstract_screen import AbstractScreen
from ...utils.number_editor import NumberEditor
from app.hardware.kippenstal_config import kippenstalConfig

class LightFromToHourScreen(AbstractScreen):

    def show(self):
        super().show()
        lcd.print('Setup light from/to', lcd.CENTER, 85)

        self._lightSchedule = [
            kippenstalConfig.getLight1From().split(':')[0],
            kippenstalConfig.getLight1From().split(':')[1],
            kippenstalConfig.getLight1To().split(':')[0],
            kippenstalConfig.getLight1To().split(':')[1],
            kippenstalConfig.getLight2From().split(':')[0],
            kippenstalConfig.getLight2From().split(':')[1],
            kippenstalConfig.getLight2To().split(':')[0],
            kippenstalConfig.getLight2To().split(':')[1],
        ]

        self._lightEditors = [
            NumberEditor(0, self._lightSchedule[0], 0, 23, '{:02d}'),
            NumberEditor(1, self._lightSchedule[1], 0, 59, '{:02d}'),
            NumberEditor(2, self._lightSchedule[2], 0, 23, '{:02d}'),
            NumberEditor(3, self._lightSchedule[3], 0, 59, '{:02d}'),
            NumberEditor(4, self._lightSchedule[4], 0, 23, '{:02d}'),
            NumberEditor(5, self._lightSchedule[5], 0, 59, '{:02d}'),
            NumberEditor(6, self._lightSchedule[6], 0, 23, '{:02d}'),
            NumberEditor(7, self._lightSchedule[7], 0, 59, '{:02d}')
        ]

        lcd.setCursor(0, 125)
        self._print('Light 1:  ', self._lightEditors[0], self._lightEditors[1], self._lightEditors[2], self._lightEditors[3])
        lcd.setCursor(0, 155)
        self._print('Light 2:  ', self._lightEditors[4], self._lightEditors[5], self._lightEditors[6], self._lightEditors[7])
        
        self._lightEditors[0].startEditing(self)

    def _print(self, prefix, fromHour, fromMinute, toHour, toMinute):
        lcd.print(prefix)
        fromHour.printToLcd()
        lcd.print(':')
        fromMinute.printToLcd()
        lcd.print(' - ')
        toHour.printToLcd()
        lcd.print(':')
        toMinute.printToLcd()

    def editingDone(self, numberEditor:NumberEditor):
        if numberEditor.nbr != 7:
            self._lightSchedule[numberEditor.nbr] = numberEditor.value
            self._lightEditors[numberEditor.nbr + 1].startEditing(self)
        else:
            self._lightSchedule[numberEditor.nbr] = numberEditor.value
            
            kippenstalConfig.setLight1From('{:02d}:{:02d}'.format(self._lightSchedule[0], self._lightSchedule[1]))
            kippenstalConfig.setLight1To('{:02d}:{:02d}'.format(self._lightSchedule[2], self._lightSchedule[3]))
            kippenstalConfig.setLight2From('{:02d}:{:02d}'.format(self._lightSchedule[4], self._lightSchedule[5]))
            kippenstalConfig.setLight2To('{:02d}:{:02d}'.format(self._lightSchedule[6], self._lightSchedule[7]))
            super().back()