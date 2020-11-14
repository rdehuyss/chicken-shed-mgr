import utime
from m5stack import lcd, buttonA, buttonB, buttonC
from machine import Timer
from .abstract_screen import AbstractScreen
from .menu_screen import MenuScreen

class MainScreen(AbstractScreen):

    def __init__(self):
        super().__init__()
        self.menu = MenuScreen()

    def show(self):
        super().show()
        buttonA.wasPressed(self.showMenu)

        self.timer = Timer(1)
        self.timer.init(period=1000, mode=Timer.PERIODIC, callback=self.time_clock)
        
    def hide(self):
        super().hide()
        buttonA.wasPressed(None)
        self.timer.deinit()

    def showMenu(self):
        self.menu.show()

    def time_clock(self, timer):
        currentTime = "{}".format(utime.strftime('%H:%M:%S', utime.localtime()))
        lcd.textClear(90, 85, '                       ', lcd.WHITE)
        lcd.setCursor(105, 85)
        lcd.print(currentTime)