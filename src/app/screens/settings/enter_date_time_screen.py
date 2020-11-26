import machine, utime
from m5stack import lcd, buttonA, buttonB, buttonC
from ..abstract_screen import AbstractScreen
from ..utils.number_editor import NumberEditor


class EditDateTimeScreen(AbstractScreen):

    def show(self):
        super().show()
        lcd.print('Setup date & time', lcd.CENTER, 85)

        self._printDate()
        self._printTime()

        self._year.startEditing(self)

    def hide(self):
        super().hide()
        buttonA.wasPressed(None)
        buttonB.wasPressed(None)
        buttonC.wasPressed(None)

    def _printDate(self):
        yearValue = 2020
        monthValue = 11
        dateValue = 7

        currentTime = utime.localtime()
        if currentTime[0] > 2000:
            yearValue = currentTime[0]
            monthValue = currentTime[1]
            dateValue = currentTime[2]

        self._year = NumberEditor(1, yearValue, 2020, 2050, '{:04d}')
        self._month = NumberEditor(2, monthValue, 1, 12, '{:02d}')
        self._date = NumberEditor(3, dateValue, 1, 31, '{:02d}')

        lcd.setCursor(75, 125)
        self._year.printToLcd()
        lcd.print('-')
        self._month.printToLcd()
        lcd.print('-')
        self._date.printToLcd()

    def _printTime(self):
        hourValue = 9
        minuteValue = 0
        secondValue = 0
        
        currentTime = utime.localtime()
        if currentTime[0] > 2000:
            hourValue = currentTime[3]
            minuteValue = currentTime[4]
            secondValue = currentTime[5]

        self._hour = NumberEditor(4, hourValue, 0, 23, '{:02d}')
        self._minute = NumberEditor(5, minuteValue, 0, 59, '{:02d}')
        self._second = NumberEditor(6, secondValue, 0, 59, '{:02d}')

        lcd.setCursor(95, 165)
        self._hour.printToLcd()
        lcd.print(':')
        self._minute.printToLcd()
        lcd.print(':')
        self._second.printToLcd()


    def editingDone(self, numberEditor:NumberEditor):
        if numberEditor.nbr == 1:
            self._month.startEditing(self)
        elif numberEditor.nbr == 2:
            self._date.startEditing(self)
        elif numberEditor.nbr == 3:
            self._hour.startEditing(self)
        elif numberEditor.nbr == 4:
            self._minute.startEditing(self)
        elif numberEditor.nbr == 5:
            self._second.startEditing(self)
        elif numberEditor.nbr == 6:
            rtc = machine.RTC()
            rtc.init((self._year.value, self._month.value, self._date.value, self._hour.value, self._minute.value, self._second.value))
            super().back()
            return

