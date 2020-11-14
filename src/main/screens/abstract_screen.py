from m5stack import lcd
from .screen_manager import ScreenManager


class AbstractScreen:

    def __init__(self):
        #print(str(self.__class__.__name__) + ' - In __init__')
        self.isShown = False

    def show(self):
        ScreenManager.isShown(self)
        self.isShown = True
        #print(str(self.__class__.__name__) + ' - In show')

        lcd.clear(lcd.WHITE)
        lcd.setColor(lcd.BLACK)
        lcd.font(lcd.FONT_Tooney, transparent=True)
        lcd.print('speckbosch', lcd.CENTER, 10)
        lcd.font(lcd.FONT_DejaVu24, transparent=True)
        lcd.print('Chicken Shed Mgr {}'.format(self._getVersion()), lcd.CENTER, 45)

    def hide(self):
        self.isShown = False
        #print(str(self.__class__.__name__) + ' - In hide')

    def back(self):
        self.hide()
        ScreenManager.back()

    def resetScreen(self, cursor:[] = [0, 85]):
        lcd.rect(cursor[0],cursor[1],320,240, lcd.WHITE, lcd.WHITE)
        lcd.setCursor(cursor[0],cursor[1])

    def _getVersion(self):
        try:
            with open('main/.version') as f:
                version = f.read()
                return version
        except:
            return '0.0'