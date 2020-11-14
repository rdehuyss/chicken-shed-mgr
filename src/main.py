import machine, utime

if utime.localtime()[0] < 2000:
    rtc = machine.RTC()
    rtc.init((2020, 11, 10, 22, 9, 5))

import main.utils.update_utils
import main.start
