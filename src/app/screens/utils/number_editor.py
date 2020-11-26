from m5stack import lcd, buttonA, buttonB, buttonC

class NumberEditor:

    def __init__(self, nbr, value, min, max, format:str, suffix=''):
        self.value = value
        self.nbr = nbr
        self._oldValue = value
        self._min = min
        self._max = max
        self._format = format
        self._suffix = suffix
        self._coord = None
        self._editingActive = False

    def printToLcdCenter(self, y):
        x = (320 - (lcd.textWidth(self._format.format(self._max) + self._suffix))) / 2
        lcd.setCursor(int(x), y)
        self.printToLcd()

    def printToLcd(self):
        if self._coord == None:
            self._coord = lcd.getCursor()

        oldTxt = self._format.format(self._oldValue) + self._suffix
        oldTxtWidth = lcd.textWidth(oldTxt)
        txt = self._format.format(self.value) + self._suffix
        txtWidth = lcd.textWidth(txt)
        # erase
        lcd.textClear(self._coord[0], self._coord[1], oldTxt, lcd.WHITE)
        lcd.line(self._coord[0], self._coord[1] + 25, self._coord[0] + oldTxtWidth, self._coord[1] + 25, lcd.WHITE)

        # write
        lcd.setCursor(self._coord[0], self._coord[1])
        lcd.print(txt)
        if self._editingActive:
            lcd.line(self._coord[0], self._coord[1] + 25, self._coord[0] + txtWidth, self._coord[1] + 25)

    def startEditing(self, screen):
        self._editingActive = True
        self._screen = screen
        self.printToLcd()
        buttonA.wasPressed(self._on_btnOk)
        buttonB.wasPressed(self._on_btnUp)
        buttonC.wasPressed(self._on_btnDown)

    def _on_btnOk(self):
        buttonA.wasPressed(None)
        buttonB.wasPressed(None)
        buttonC.wasPressed(None)
        self._editingActive = False
        self.printToLcd()
        self._screen.editingDone(self)

    def _on_btnUp(self):
        self._oldValue = self.value
        if self._max == self.value:
            self.value = self._min
        else:
            self.value = self.value + 1
        self.printToLcd()

    def _on_btnDown(self):
        self._oldValue = self.value
        if self._min == self.value:
            self.value = self._max
        else:
            self.value = self.value - 1
        self.printToLcd()