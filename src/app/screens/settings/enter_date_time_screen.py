import machine, utime
from m5stack import lcd, buttonA, buttonB, buttonC
from ..abstract_screen import AbstractScreen
from ..utils.number_editor import NumberEditor


class EditDateTimeScreen(AbstractScreen):

    def show(self):
        super().show()
        lcd.print('Setup date & time', lcd.CENTER, 85)

        self._initDateTimeEditors()
        self._printDate()
        self._printTime()

        self. self._dateTimeEditors[0].startEditing(self)

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
            self._dateTimeEditors[0].value = currentDateTime[0]
            self._dateTimeEditors[1].value = currentDateTime[1]
            self._dateTimeEditors[2].value = currentDateTime[2]
            self._dateTimeEditors[3].value = currentDateTime[3]
            self._dateTimeEditors[4].value = currentDateTime[4]
            self._dateTimeEditors[5].value = currentDateTime[5]

    def _printDate(self):
        lcd.setCursor(75, 125)
        self._dateTimeEditors[0].printToLcd()
        lcd.print('-')
        self._dateTimeEditors[1].printToLcd()
        lcd.print('-')
        self._dateTimeEditors[2].printToLcd()

    def _printTime(self):
        lcd.setCursor(95, 165)
        self._dateTimeEditors[3].printToLcd()
        lcd.print(':')
        self._dateTimeEditors[4].printToLcd()
        lcd.print(':')
        self._dateTimeEditors[5].printToLcd()

    def editingDone(self, numberEditor:NumberEditor):
        if numberEditor.nbr < 6:
            self._dateTimeEditors[numberEditor.nbr + 1].startEditing(self)
        else:
            rtc = machine.RTC()
            rtc.init((
                self._dateTimeEditors[0].value, self._dateTimeEditors[1].value, self._dateTimeEditors[2].value, 
                self._dateTimeEditors[3].value, self._dateTimeEditors[4].value, self._dateTimeEditors[5].value))
            super().back()
            return
