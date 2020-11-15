from m5stack import *
from ...abstract_screen import AbstractScreen
from ...utils.number_editor import NumberEditor
from app.hardware.kippenstal_config import kippenstalConfig

class DoorOpenFromToHourScreen(AbstractScreen):

    def __init__(self):
        super().__init__()

    def show(self):
        super().show()
        lcd.print('Set Door Open', lcd.CENTER, 85)

        self.fromHourEditor = NumberEditor(1, kippenstalConfig.getDoorOpenAtHour(), 0, 23, '{:02d}', 'h')
        self.toHourEditor = NumberEditor(2, kippenstalConfig.getDoorCloseAtHour(), 0, 12, '{:02d}', 'h aft sunset')

        self.fromHourEditor.printToLcdCenter(125)
        lcd.print('\n')
        self.toHourEditor.printToLcdCenter(165)
        self.fromHourEditor.startEditing(self)


    def editingDone(self, numberEditor:NumberEditor):
        if numberEditor.nbr == 1:
            kippenstalConfig.setDoorOpenAtHour(self.fromHourEditor.value)
            self.toHourEditor.startEditing(self)
        elif numberEditor.nbr == 2:
            kippenstalConfig.setDoorCloseAtHour(self.toHourEditor.value)
            super().back()
