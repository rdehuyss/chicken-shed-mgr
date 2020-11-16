import machine, utime

if utime.localtime()[0] < 2000:
    rtc = machine.RTC()
    rtc.init((2020, 11, 10, 22, 9, 5))

import app.utils.update_utils
import app.start

from app.utils.ota_logger import OTALogger

o = OTALogger('b5b29d316b4a0f61a8be264f236a2376', '245f173c2937fec397b5b58dbf0e97e4b5360520')



