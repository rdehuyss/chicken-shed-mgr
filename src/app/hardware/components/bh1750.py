"""
Micropython BH1750 ambient light sensor driver.
from https://github.com/PinkInk/upylib/tree/master/bh1750
"""

from utime import sleep_ms


class BH1750():
    """Micropython BH1750 ambient light sensor driver."""

    _PWR_OFF = 0x00
    _PWR_ON = 0x01
    _RESET = 0x07

    # modes
    CONT_LOWRES = 0x13
    CONT_HIRES_1 = 0x10
    CONT_HIRES_2 = 0x11
    ONCE_HIRES_1 = 0x20
    ONCE_HIRES_2 = 0x21
    ONCE_LOWRES = 0x23

    # default addr=0x23 if addr pin floating or pulled to ground
    # addr=0x5c if addr pin pulled high
    def __init__(self, bus, addr=0x23):
        self._bus = bus
        self._addr = addr
        self.off()
        self.reset()

    def off(self):
        """Turn sensor off."""
        self._set_mode(self._PWR_OFF)

    def on(self):
        """Turn sensor on."""
        self._set_mode(self._PWR_ON)

    def reset(self):
        """Reset sensor, turn on first if required."""
        self.on()
        self._set_mode(self._RESET)

    def _set_mode(self, mode):
        """Set sensor mode."""
        self._mode = mode
        self._bus.writeto(self._addr, bytes([self._mode]))

    def luminance(self, mode):
        """Sample luminance (in lux), using specified sensor mode."""
        # continuous modes
        if mode & 0x10 and mode != self._mode:
            self._set_mode(mode)
        # one shot modes
        if mode & 0x20:
            self._set_mode(mode)
        # earlier measurements return previous reading
        sleep_ms(24 if mode in (0x13, 0x23) else 180)
        data = self._bus.readfrom(self._addr, 2)
        factor = 2.0 if mode in (0x11, 0x21) else 1.0
        return (data[0]<<8 | data[1]) / (1.2 * factor)