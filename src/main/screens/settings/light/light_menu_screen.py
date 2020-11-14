from ...abstract_menu_screen import AbstractMenuScreen
from .light_test_screen import LightTestScreen
from .light_schedule_enabled_screen import LightScheduleEnabledScreen
from .light_threshold_screen import LightThresholdScreen
from .light_set_from_to_screen import LightFromToHourScreen
from main.hardware.kippenstal_config import kippenstalConfig

class LightMenuScreen(AbstractMenuScreen):

    def __init__(self):
        super().__init__()
        self.lightTestScreen = LightTestScreen()
        self.lightScheduleEnabledScreen = LightScheduleEnabledScreen()
        self.lightThresholdScreen = LightThresholdScreen()
        self.lightFromToHourScreen = LightFromToHourScreen()

    def getMenuItems(self):
        return [
                ('Test Lights', self.lightTestScreen.show),
                ('Light Schedule - {}'.format('on' if kippenstalConfig.isLightScheduleEnabled() else 'off'), self.lightScheduleEnabledScreen.show),
                ('Setup Light Threshold', self.lightThresholdScreen.show, kippenstalConfig.isLightScheduleEnabled()),
                ('Setup From/To Time', self.lightFromToHourScreen.show, kippenstalConfig.isLightScheduleEnabled()),
                ('Back', super().back)
            ]
