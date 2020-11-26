from ...abstract_menu_screen import AbstractMenuScreen
from app.hardware.kippenstal import kippenstal

class FenceTestScreen(AbstractMenuScreen):

    def getMenuItems(self):
        return [
                ('Fence on', self._turnFenceOn),
                ('Fence off', self._turnFenceOff),
                ('Back', super().back)
            ]
    
    def show(self):
        super().show()
        kippenstal.stop()

    def hide(self):
        super().hide()
        kippenstal.start()

    def _turnFenceOn(self):
        kippenstal.fence.on()

    def _turnFenceOff(self):
        kippenstal.fence.off()
