import gc, utime
from machine import Timer
from .screens.main_screen import MainScreen
from .hardware.kippenstal import kippenstal

mainScreen = MainScreen()
mainScreen.show()

def run_updates(timer):
    mainScreen.update_clock()
    kippenstal.evaluate()
    gc.collect()

timer = Timer(1)
timer.init(period=1000, mode=Timer.PERIODIC, callback=run_updates)