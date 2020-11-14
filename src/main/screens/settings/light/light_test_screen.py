from ...abstract_menu_screen import AbstractMenuScreen
from main.hardware.kippenstal import kippenstal

class LightTestScreen(AbstractMenuScreen):

    def getMenuItems(self):
        return [
                ('Light on', self.turnLightOn),
                ('Light off', self.turnLightOff),
                ('Back', super().back)
            ]
    
    def show(self):
        super().show()
        kippenstal.stop()

    def hide(self):
        super().hide()
        kippenstal.start()

    def turnLightOn(self):
        kippenstal.light.on()

    def turnLightOff(self):
        kippenstal.light.off()
