from m5stack import lcd, buttonA, buttonB, buttonC

class StringSelector:

    def __init__(self, value, possibleValues):
        self.value = value
        self._oldValue = value
        self._possibleValues = possibleValues
        self._index = possibleValues.index(value)
        self._coord = None
        self._editingActive = False

    def printToLcd(self):
        if self._coord == None:
            self._coord = lcd.getCursor()

        oldTxt = self._oldValue
        oldTxtWith = lcd.textWidth(oldTxt)
        txt = self.value
        txtWidth = lcd.textWidth(txt)
        # erase
        lcd.textClear(self._coord[0], self._coord[1], oldTxt, lcd.WHITE)
        lcd.line(self._coord[0], self._coord[1] + 25, self._coord[0] + oldTxtWith, self._coord[1] + 25, lcd.WHITE)

        # write
        x = (320 - (lcd.textWidth(self.value))) / 2
        lcd.setCursor(int(x), self._coord[1])
        self._coord = lcd.getCursor()
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
        if len(self._possibleValues) == self._index + 1:
            self._index = 0
        else:
            self._index = self._index + 1
        self.value = self._possibleValues[self._index]
        self.printToLcd()

    def _on_btnDown(self):
        self._oldValue = self.value
        if 0 == self._index:
            self._index = (len(self._possibleValues) - 1)
        else:
            self._index = self._index - 1
        self.value = self._possibleValues[self._index]
        self.printToLcd()