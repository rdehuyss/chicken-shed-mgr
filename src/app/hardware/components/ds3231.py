# ds3231_port.py Portable driver for DS3231 precison real time clock.
# Adapted from WiPy driver at https://github.com/scudderfish/uDS3231

# Author: Peter Hinch
# Copyright Peter Hinch 2018 Released under the MIT license.

import utime
import machine
import sys
DS3231_I2C_ADDR = 104

try:
    rtc = machine.RTC()
except:
    print('Warning: machine module does not support the RTC.')
    rtc = None

def bcd2dec(bcd):
    return (((bcd & 0xf0) >> 4) * 10 + (bcd & 0x0f))

def dec2bcd(dec):
    tens, units = divmod(dec, 10)
    return (tens << 4) + units

def tobytes(num):
    return num.to_bytes(1, 'little')

class DS3231:
    def __init__(self, i2c):
        self.i2c = i2c
        self.timebuf = bytearray(7)
        if DS3231_I2C_ADDR not in self.i2c.scan():
            raise RuntimeError("DS3231 not found on I2C bus at %d" % DS3231_I2C_ADDR)

    def get_time(self, set_rtc=False):
        if set_rtc:
            self.await_transition()  # For accuracy set RTC immediately after a seconds transition
        else:
            self.i2c.readfrom_mem_into(DS3231_I2C_ADDR, 0, self.timebuf) # don't wait
        return self.convert(set_rtc)

    def convert(self, set_rtc=False):  # Return a tuple in localtime() format (less yday)
        data = self.timebuf
        ss = bcd2dec(data[0])
        mm = bcd2dec(data[1])
        if data[2] & 0x40:
            hh = bcd2dec(data[2] & 0x1f)
            if data[2] & 0x20:
                hh += 12
        else:
            hh = bcd2dec(data[2])
        wday = data[3]
        DD = bcd2dec(data[4])
        MM = bcd2dec(data[5] & 0x1f)
        YY = bcd2dec(data[6])
        if data[5] & 0x80:
            YY += 2000
        else:
            YY += 1900
        # Time from DS3231 in time.localtime() format (less yday)
        result = YY, MM, DD, hh, mm, ss, wday -1, 0
        if set_rtc:
            if rtc is None:
                # Best we can do is to set local time
                secs = utime.mktime(result)
                utime.localtime(secs)
            else:
                rtc.init((YY, MM, DD, hh, mm, ss))
        return result

    def save_time(self):
        (YY, MM, mday, hh, mm, ss, wday, yday) = utime.localtime()  # Based on RTC
        self.i2c.writeto_mem(DS3231_I2C_ADDR, 0, tobytes(dec2bcd(ss)))
        self.i2c.writeto_mem(DS3231_I2C_ADDR, 1, tobytes(dec2bcd(mm)))
        self.i2c.writeto_mem(DS3231_I2C_ADDR, 2, tobytes(dec2bcd(hh)))  # Sets to 24hr mode
        self.i2c.writeto_mem(DS3231_I2C_ADDR, 3, tobytes(dec2bcd(wday + 1)))  # 1 == Monday, 7 == Sunday
        self.i2c.writeto_mem(DS3231_I2C_ADDR, 4, tobytes(dec2bcd(mday)))  # Day of month
        if YY >= 2000:
            self.i2c.writeto_mem(DS3231_I2C_ADDR, 5, tobytes(dec2bcd(MM) | 0b10000000))  # Century bit
            self.i2c.writeto_mem(DS3231_I2C_ADDR, 6, tobytes(dec2bcd(YY-2000)))
        else:
            self.i2c.writeto_mem(DS3231_I2C_ADDR, 5, tobytes(dec2bcd(MM)))
            self.i2c.writeto_mem(DS3231_I2C_ADDR, 6, tobytes(dec2bcd(YY-1900)))

    # Wait until DS3231 seconds value changes before reading and returning data
    def await_transition(self):
        self.i2c.readfrom_mem_into(DS3231_I2C_ADDR, 0, self.timebuf)
        ss = self.timebuf[0]
        while ss == self.timebuf[0]:
            self.i2c.readfrom_mem_into(DS3231_I2C_ADDR, 0, self.timebuf)
        return self.timebuf

    def get_temperature(self):
        t = self.i2c.readfrom_mem(DS3231_I2C_ADDR, 0x11, 2)
        i = t[0] << 8 | t[1]
        return self._twos_complement(i >> 6, 10) * 0.25

    def _twos_complement(self, input_value: int, num_bits: int) -> int:
        mask = 2 ** (num_bits - 1)
        return -(input_value & mask) + (input_value & ~mask)