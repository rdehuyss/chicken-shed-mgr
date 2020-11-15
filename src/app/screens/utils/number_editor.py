from m5stack import lcd, buttonA, buttonB, buttonC

class NumberEditor:

    def __init__(self, nbr, value, min, max, format:str, suffix=''):
        self.value = value
        self.oldValue = value
        self.nbr = nbr
        self.min = min
        self.max = max
        self.format = format
        self.suffix = suffix
        self.coord = None
        self.editingActive = False

    def printToLcdCenter(self, y):
        x = (320 - (lcd.textWidth(self.format.format(self.max) + self.suffix))) / 2
        lcd.setCursor(int(x), y)
        self.printToLcd()

    def printToLcd(self):
        if self.coord == None:
            self.coord = lcd.getCursor()

        oldTxt = self.format.format(self.oldValue) + self.suffix
        oldTxtWidth = lcd.textWidth(oldTxt)
        txt = self.format.format(self.value) + self.suffix
        txtWidth = lcd.textWidth(txt)
        # erase
        lcd.textClear(self.coord[0], self.coord[1], oldTxt, lcd.WHITE)
        lcd.line(self.coord[0], self.coord[1] + 25, self.coord[0] + oldTxtWidth, self.coord[1] + 25, lcd.WHITE)

        # write
        lcd.setCursor(self.coord[0], self.coord[1])
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
        if self.max == self.value:
            self.value = self.min
        else:
            self.value = self.value + 1
        self.printToLcd()

    def on_btnDown(self):
        self.oldValue = self.value
        if self.min == self.value:
            self.value = self.max
        else:
            self.value = self.value - 1
        self.printToLcd()