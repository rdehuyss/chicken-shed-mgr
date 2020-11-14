from m5stack import lcd, buttonA, buttonB, buttonC

class StringSelector:

    def __init__(self, value, possibleValues):
        self.value = value
        self.oldValue = value
        self.possibleValues = possibleValues
        self.index = possibleValues.index(value)
        self.coord = None
        self.editingActive = False

    def printToLcd(self):
        if self.coord == None:
            self.coord = lcd.getCursor()

        oldTxt = self.oldValue
        oldTxtWith = lcd.textWidth(oldTxt)
        txt = self.value
        txtWidth = lcd.textWidth(txt)
        # erase
        lcd.textClear(self.coord[0], self.coord[1], oldTxt, lcd.WHITE)
        lcd.line(self.coord[0], self.coord[1] + 25, self.coord[0] + oldTxtWith, self.coord[1] + 25, lcd.WHITE)

        # write
        x = (320 - (lcd.textWidth(self.value))) / 2
        lcd.setCursor(int(x), self.coord[1])
        self.coord = lcd.getCursor()
        lcd.print(txt)
        if self.editingActive:
            lcd.line(self.coord[0], self.coord[1] + 25, self.coord[0] + txtWidth, self.coord[1] + 25)

    def startEditing(self, screen):
        self.editingActive = True
        self.screen = screen
        self.printToLcd()
        buttonA.wasPressed(self.on_btnOk)
        buttonB.wasPressed(self.on_btnUp)
        buttonC.wasPressed(self.on_btnDown)

    def on_btnOk(self):
        buttonA.wasPressed(None)
        buttonB.wasPressed(None)
        buttonC.wasPressed(None)
        self.editingActive = False
        self.printToLcd()
        self.screen.editingDone(self)

    def on_btnUp(self):
        self.oldValue = self.value
        if len(self.possibleValues) == self.index + 1:
            self.index = 0
        else:
            self.index = self.index + 1
        self.value = self.possibleValues[self.index]
        self.printToLcd()

    def on_btnDown(self):
        self.oldValue = self.value
        if 0 == self.index:
            self.index = (len(self.possibleValues) - 1)
        else:
            self.index = self.index - 1
        self.value = self.possibleValues[self.index]
        self.printToLcd()