from ...abstract_menu_screen import AbstractMenuScreen
from .light_test_screen import LightTestScreen
from .light_schedule_enabled_screen import LightScheduleEnabledScreen
from .light_threshold_screen import LightThresholdScreen
from .light_set_from_to_screen import LightFromToHourScreen
from app.hardware.kippenstal_config import kippenstalConfig

class LightMenuScreen(AbstractMenuScreen):

    def __init__(self):
        super().__init__()
        self._lightTestScreen = LightTestScreen()
        self._lightScheduleEnabledScreen = LightScheduleEnabledScreen()
        self._lightThresholdScreen = LightThresholdScreen()
        self._lightFromToHourScreen = LightFromToHourScreen()

    def getMenuItems(self):
        return [
                ('Test Lights', self._lightTestScreen.show),
                ('Light Schedule - {}'.format('on' if kippenstalConfig.isLightScheduleEnabled() else 'off'), self._lightScheduleEnabledScreen.show),
                ('Setup Light Threshold', self._lightThresholdScreen.show, kippenstalConfig.isLightScheduleEnabled()),
                ('Setup From/To Time', self._lightFromToHourScreen.show, kippenstalConfig.isLightScheduleEnabled()),
                ('Back', super().back)
            ]
