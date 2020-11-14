import machine, utime
from m5stack import *
from ..abstract_screen import AbstractScreen
from ..utils.number_editor import NumberEditor


class EditDateTimeScreen(AbstractScreen):

    def show(self):
        super().show()
        lcd.print('Setup date & time', lcd.CENTER, 85)

        self.printDate()
        self.printTime()

        self.year.startEditing(self)

    def hide(self):
        super().hide()
        buttonA.wasPressed(None)
        buttonB.wasPressed(None)
        buttonC.wasPressed(None)

    def printDate(self):
        yearValue = 2020
        monthValue = 11
        dateValue = 7

        currentTime = utime.localtime()
        if currentTime[0] > 2000:
            yearValue = currentTime[0]
            monthValue = currentTime[1]
            dateValue = currentTime[2]

        self.year = NumberEditor(1, yearValue, 2020, 2050, '{:04d}')
        self.month = NumberEditor(2, monthValue, 1, 12, '{:02d}')
        self.date = NumberEditor(3, dateValue, 1, 31, '{:02d}')

        lcd.setCursor(75, 125)
        self.year.printToLcd()
        lcd.print('-')
        self.month.printToLcd()
        lcd.print('-')
        self.date.printToLcd()

    def printTime(self):
        hourValue = 9
        minuteValue = 0
        secondValue = 0
        
        currentTime = utime.localtime()
        if currentTime[0] > 2000:
            hourValue = currentTime[3]
            minuteValue = currentTime[4]
            secondValue = currentTime[5]

        self.hour = NumberEditor(4, hourValue, 0, 23, '{:02d}')
        self.minute = NumberEditor(5, minuteValue, 0, 59, '{:02d}')
        self.second = NumberEditor(6, secondValue, 0, 59, '{:02d}')

        lcd.setCursor(95, 165)
        self.hour.printToLcd()
        lcd.print(':')
        self.minute.printToLcd()
        lcd.print(':')
        self.second.printToLcd()


    def editingDone(self, numberEditor:NumberEditor):
        if numberEditor.nbr == 1:
            self.month.startEditing(self)
        elif numberEditor.nbr == 2:
            self.date.startEditing(self)
        elif numberEditor.nbr == 3:
            self.hour.startEditing(self)
        elif numberEditor.nbr == 4:
            self.minute.startEditing(self)
        elif numberEditor.nbr == 5:
            self.second.startEditing(self)
        elif numberEditor.nbr == 6:
            rtc = machine.RTC()
            rtc.init((self.year.value, self.month.value, self.date.value, self.hour.value, self.minute.value, self.second.value))
            super().back()
            return

