import machine, utime
from m5stack import lcd, buttonA, buttonB, buttonC
from ..abstract_screen import AbstractScreen
from ..utils.number_editor import NumberEditor


class EditDateTimeScreen(AbstractScreen):

    def show(self):
        super().show()
        lcd.print('Setup date & time', lcd.CENTER, 85)

        self._initDateTimeEditors()
        self._print((75, 125), self._dateTimeEditors[0], self._dateTimeEditors[1], self._dateTimeEditors[2], '-')
        self._print((95, 165), self._dateTimeEditors[3], self._dateTimeEditors[4], self._dateTimeEditors[5], ':')

        self._dateTimeEditors[0].startEditing(self)

    def hide(self):
        super().hide()
        buttonA.wasPressed(None)
        buttonB.wasPressed(None)
        buttonC.wasPressed(None)

    def _initDateTimeEditors(self):
        currentDateTime = utime.localtime()
        if not hasattr(self, '_dateTimeEditors'):
            self._dateTimeEditors = [
                NumberEditor(0, currentDateTime[0], 2020, 2050, '{:04d}'),
                NumberEditor(1, currentDateTime[1], 1, 12, '{:02d}'),
                NumberEditor(2, currentDateTime[2], 1, 31, '{:02d}'),
                NumberEditor(3, currentDateTime[3], 0, 23, '{:02d}'),
                NumberEditor(4, currentDateTime[4], 0, 59, '{:02d}'),
                NumberEditor(5, currentDateTime[5], 0, 59, '{:02d}')
            ]
        else:
            for i in range(len(self._dateTimeEditors)):
                self._dateTimeEditors[i].value = currentDateTime[i]

    def _print(self, cursor, editor1, editor2, editor3, separator):
        lcd.setCursor(cursor[0], cursor[1])
        editor1.printToLcd()
        lcd.print(separator)
        editor2.printToLcd()
        lcd.print(separator)
        editor3.printToLcd()

    def editingDone(self, numberEditor:NumberEditor):
        if numberEditor.nbr < 5:
            self._dateTimeEditors[numberEditor.nbr + 1].startEditing(self)
        else:
            rtc = machine.RTC()
            rtc.init((
                self._dateTimeEditors[0].value, self._dateTimeEditors[1].value, self._dateTimeEditors[2].value, 
                self._dateTimeEditors[3].value, self._dateTimeEditors[4].value, self._dateTimeEditors[5].value))
            
            from ...hardware.kippenstal import kippenstal
            kippenstal.saveTime()

            super().back()
            return
