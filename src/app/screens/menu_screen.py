from .abstract_menu_screen import AbstractMenuScreen
from .settings.enter_date_time_screen import EditDateTimeScreen
from .settings.light.light_menu_screen import LightMenuScreen
from .settings.fence.fence_menu_screen import FenceMenuScreen
from .settings.door.door_menu_screen import DoorOpenerMenuScreen
from .update.update_screen import UpdateScreen1

class MenuScreen(AbstractMenuScreen):

    def __init__(self):
        super().__init__()
        self.editDateTimeScreen = EditDateTimeScreen()
        self.lightMenuScreen = LightMenuScreen()
        self.fenceMenuScreen = FenceMenuScreen()
        self.doorOpenerMenuScreen = DoorOpenerMenuScreen()
        self.updateScreen = UpdateScreen1()

    def getMenuItems(self):
        return [
                ('Setup date & time', self.editDateTimeScreen.show),
                ('Setup lights', self.lightMenuScreen.show),
                ('Setup fence', self.fenceMenuScreen.show),
                ('Setup door opener', self.doorOpenerMenuScreen.show),
                ('Update', self.updateScreen.show),
                ('Back', super().back)
            ]
