from .abstract_menu_screen import AbstractMenuScreen
from .settings.enter_date_time_screen import EditDateTimeScreen
from .settings.light.light_menu_screen import LightMenuScreen
from .settings.fence.fence_menu_screen import FenceMenuScreen
from .settings.door.door_menu_screen import DoorOpenerMenuScreen
from .update.update_screen import UpdateScreen1

class MenuScreen(AbstractMenuScreen):

    def __init__(self):
        super().__init__()
        self._editDateTimeScreen = EditDateTimeScreen()
        self._lightMenuScreen = LightMenuScreen()
        self._fenceMenuScreen = FenceMenuScreen()
        self._doorOpenerMenuScreen = DoorOpenerMenuScreen()
        self._updateScreen = UpdateScreen1()

    def getMenuItems(self):
        return [
                ('Setup date & time', self._editDateTimeScreen.show),
                ('Setup lights', self._lightMenuScreen.show),
                ('Setup fence', self._fenceMenuScreen.show),
                ('Setup door opener', self._doorOpenerMenuScreen.show),
                ('Update', self._updateScreen.show),
                ('Back', super().back)
            ]
