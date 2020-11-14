from ...abstract_menu_screen import AbstractMenuScreen
from main.hardware.kippenstal import kippenstal

class FenceTestScreen(AbstractMenuScreen):

    def getMenuItems(self):
        return [
                ('Fence on', self.turnFenceOn),
                ('Fence off', self.turnFenceOff),
                ('Back', super().back)
            ]
    
    def show(self):
        super().show()
        kippenstal.stop()

    def hide(self):
        super().hide()
        kippenstal.start()

    def turnFenceOn(self):
        kippenstal.fence.on()

    def turnFenceOff(self):
        kippenstal.fence.off()
