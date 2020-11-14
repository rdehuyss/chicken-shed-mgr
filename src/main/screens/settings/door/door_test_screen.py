from ...abstract_menu_screen import AbstractMenuScreen
from main.hardware.kippenstal import kippenstal

class DoorOpenerTestScreen(AbstractMenuScreen):

    def getMenuItems(self):
        return [
                ('Open Door', self.openDoor),
                ('Close Door', self.closeDoor),
                ('Back', super().back)
            ]
    
    def show(self):
        super().show()
        kippenstal.stop()

    def hide(self):
        super().hide()
        kippenstal.start()

    def openDoor(self):
        kippenstal.doorOpener.open()

    def closeDoor(self):
        kippenstal.doorOpener.close()
