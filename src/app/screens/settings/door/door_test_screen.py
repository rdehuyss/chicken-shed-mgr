from ...abstract_menu_screen import AbstractMenuScreen
from app.hardware.kippenstal import kippenstal

class DoorOpenerTestScreen(AbstractMenuScreen):

    def getMenuItems(self):
        return [
                ('Open Door', self._openDoor),
                ('Close Door', self._closeDoor),
                ('Back', super().back)
            ]
    
    def show(self):
        super().show()
        kippenstal.stop()

    def hide(self):
        super().hide()
        kippenstal.start()

    def _openDoor(self):
        kippenstal.doorOpener.open()

    def _closeDoor(self):
        kippenstal.doorOpener.close()
