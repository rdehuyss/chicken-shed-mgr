from m5stack import lcd
from ...abstract_screen import AbstractScreen
from ...utils.number_editor import NumberEditor
from app.hardware.kippenstal_config import kippenstalConfig

class DoorOpenFromToHourScreen(AbstractScreen):

    def __init__(self):
        super().__init__()

    def show(self):
        super().show()
        lcd.print('Set Door Open', lcd.CENTER, 85)

        self._fromHourEditor = NumberEditor(1, kippenstalConfig.getDoorOpenAtHour(), 0, 23, '{:02d}', 'h')
        self._toHourEditor = NumberEditor(2, kippenstalConfig.getDoorCloseAtHour(), 0, 12, '{:02d}', 'h aft sunset')

        self._fromHourEditor.printToLcdCenter(125)
        lcd.print('\n')
        self._toHourEditor.printToLcdCenter(165)
        self._fromHourEditor.startEditing(self)


    def editingDone(self, numberEditor:NumberEditor):
        if numberEditor.nbr == 1:
            kippenstalConfig.setDoorOpenAtHour(self._fromHourEditor.value)
            self._toHourEditor.startEditing(self)
        elif numberEditor.nbr == 2:
            kippenstalConfig.setDoorCloseAtHour(self._toHourEditor.value)
            super().back()
