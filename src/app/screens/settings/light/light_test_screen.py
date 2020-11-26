from ...abstract_menu_screen import AbstractMenuScreen
from app.hardware.kippenstal import kippenstal

class LightTestScreen(AbstractMenuScreen):

    def getMenuItems(self):
        return [
                ('Light on', self._turnLightOn),
                ('Light off', self._turnLightOff),
                ('Back', super().back)
            ]
    
    def show(self):
        super().show()
        kippenstal.stop()

    def hide(self):
        super().hide()
        kippenstal.start()

    def _turnLightOn(self):
        kippenstal.light.on()

    def _turnLightOff(self):
        kippenstal.light.off()
