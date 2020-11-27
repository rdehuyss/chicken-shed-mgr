import utime
from m5stack import lcd, buttonA, buttonB, buttonC
from .abstract_screen import AbstractScreen
from .menu_screen import MenuScreen
from ..hardware.kippenstal import kippenstal

class MainScreen(AbstractScreen):

    def __init__(self):
        super().__init__()

    def show(self):
        super().show()
        self._showOptions()
        
    def hide(self):
        super().hide()
        buttonA.wasPressed(None)

    def _showOptions(self):
        menu = MenuScreen()
        buttonA.wasPressed(menu.show)
        lcd.image(50, 205, 'imgs/menu.bmp')

        buttonB.wasPressed(kippenstal.doorOpener.toggle)
        lcd.image(145,205,'imgs/door.bmp')

        buttonC.wasPressed(kippenstal.light.toggle)
        lcd.image(243,205,'imgs/lightbulb-outline.bmp')

    def update_clock(self):
        if self._isShown:
            lcd.textClear(90, 85, '                       ', lcd.WHITE)
            lcd.setCursor(105, 85)
            lcd.print("{}".format(utime.strftime('%H:%M:%S', utime.localtime())))
        