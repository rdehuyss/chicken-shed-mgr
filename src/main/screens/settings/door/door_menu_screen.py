from ...abstract_menu_screen import AbstractMenuScreen
from .door_test_screen import DoorOpenerTestScreen
from .door_schedule_enabled_screen import DoorScheduleEnabledScreen
from .door_open_from_to_screen import DoorOpenFromToHourScreen
from main.hardware.kippenstal_config import kippenstalConfig

class DoorOpenerMenuScreen(AbstractMenuScreen):

    def __init__(self):
        super().__init__()
        self.doorOpenerTestScreen = DoorOpenerTestScreen()
        self.doorScheduledEnabledScreen = DoorScheduleEnabledScreen()
        self.doorOpenFromToHourScreen = DoorOpenFromToHourScreen()

    def getMenuItems(self):
        return [
                ('Test Door Opener', self.doorOpenerTestScreen.show),
                ('Door Schedule - {}'.format('on' if kippenstalConfig.isDoorOpenerScheduleEnabled() else 'off'), self.doorScheduledEnabledScreen.show),
                ('Door Open from/to', self.doorOpenFromToHourScreen.show, kippenstalConfig.isDoorOpenerScheduleEnabled()),
                ('Back', super().back)
            ]

    
