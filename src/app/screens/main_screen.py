import utime
from m5stack import lcd, buttonA, buttonB, buttonC
from .abstract_screen import AbstractScreen
from .menu_screen import MenuScreen
from ..hardware.kippenstal import kippenstal

class MainScreen(AbstractScreen):

    def __init__(self):
        super().__init__()
        self._menu = MenuScreen()
        self._isSleeping = False
        self._lastInteraction = utime.time()

    def show(self):
        super().show()
        self._lastInteraction = utime.time()
        self._showOptions()
        
    def hide(self):
        super().hide()
        buttonA.wasPressed(None)
        buttonB.wasPressed(None)
        buttonC.wasPressed(None)

    def _showOptions(self):
        buttonA.wasPressed(self._menu.show)
        lcd.image(50, 205, 'imgs/menu.bmp')

        buttonB.wasPressed(kippenstal.doorOpener.toggle)
        lcd.image(145,205,'imgs/door.bmp')

        buttonC.wasPressed(kippenstal.light.toggle)
        lcd.image(243,205,'imgs/lightbulb-outline.bmp')

    def _wake(self):
        self._isSleeping = False
        self._lastInteraction = utime.time()
        self._showOptions()
        self.update_clock()
        lcd.backlight(50)

    def _sleep(self):
        self._isSleeping = True
        lcd.backlight(0)
        buttonA.wasPressed(self._wake)
        buttonB.wasPressed(self._wake)
        buttonC.wasPressed(self._wake)

    def update_clock(self):
        if self._isShown:
            if self._isSleeping:
                return
            elif self._lastInteraction + 120 < utime.time():
                self._sleep()
            else:
                lcd.textClear(90, 85, '                       ', lcd.WHITE)
                lcd.setCursor(105, 85)
                lcd.print("{}".format(utime.strftime('%H:%M:%S', utime.localtime())))
                lcd.setCursor(112, 115)
                lcd.print("{} C".format(kippenstal.getTemperature()))

