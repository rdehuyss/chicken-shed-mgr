import machine, utime, main.secrets as secrets
from m5stack import *
from ..abstract_screen import AbstractScreen
from ..abstract_menu_screen import AbstractMenuScreen

class UpdateScreen1(AbstractMenuScreen):

    def __init__(self):
        super().__init__()
        self.updateScreen2 = UpdateScreen2()

    def printHeader(self):
        lcd.font(lcd.FONT_DejaVu18, transparent=True)
        lcd.println('Upload logs and check for a new\nversion of Chicken Shed Mgr.')
        

    def getMenuItems(self):
        return [
                ('OK', self.updateScreen2.show),
                ('Back', super().back)
            ]


class UpdateScreen2(AbstractMenuScreen):

    def __init__(self):
        super().__init__()
        self.updateScreen3 = UpdateScreen3()
    
    def printHeader(self):
        lcd.font(lcd.FONT_DejaVu18, transparent=True)
        lcd.println('Please create a WIFI AP using\nyour phone:')
        lcd.println('- SSID = ' + str(secrets.WIFI_SSID))
        lcd.println('- Pw = ' + str(secrets.WIFI_PASSWORD))
        

    def getMenuItems(self):
        return [
                ('OK', self.updateScreen3.show),
                ('Back', super().back)
            ]

class UpdateScreen3(AbstractScreen):
    
    def show(self):
        super().show()
        lcd.font(lcd.FONT_DejaVu18, transparent=True)
        self.resetScreen()
        lcd.print('Connecting to wifi...')
        
        import network
        sta_if = network.WLAN(network.STA_IF)
        sta_if.active(True)
        sta_if.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)

        startTime = utime.time()
        while not sta_if.isconnected():
            if startTime + 45 < utime.time():
                break

            lcd.print('.')
            utime.sleep(2)
            sta_if.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)

        if sta_if.isconnected():
            self.resetScreen()
            lcd.println('Connected to WIFI...')
            lcd.println('Machine will reboot!')
            lcd.println('Stay until update done')
            with open('.updateRequested', mode='a'):
                pass
            utime.sleep(5)
            machine.reset()
        else:
            self.resetScreen()
            lcd.print('Could not connect to WIFI!')
            utime.sleep(5)
            super().back()