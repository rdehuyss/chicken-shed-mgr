import machine, utime, os

if utime.localtime()[0] < 2000:
    rtc = machine.RTC()
    rtc.init((2020, 11, 10, 22, 9, 5))

WIFI_SSID = 'AndroidRD'
WIFI_PASSWORD = 'internetisvaniedereen'

#3f024f6ca347c9d489078837d335a5f6a03f2e59

try:
    with open('.updateRequested', "r") as updateNeeded:
        try:
            print('wil update')
            import network
            from main.utils.httpclient import HttpClient

            sta_if = network.WLAN(network.STA_IF)
            sta_if.active(True)
            sta_if.connect(WIFI_SSID, WIFI_PASSWORD)

            startTime = utime.time()
            while not sta_if.isconnected():
                if startTime + 45 < utime.time():
                    break

                utime.sleep(2)
                sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
            
            rtc = machine.RTC()
            rtc.ntp_sync(server="0.be.pool.ntp.org", tz="CET-1CEST,M3.5.0,M10.5.0/3")
        
            httpclient = HttpClient()
            httpclient.post('https://ptsv2.com/t/chicken-shed/post', file='logs.log')
            print('logs uploaded')
        except BaseException as error:
            print(error)
            print('update failed')

    os.remove('.updateRequested')
    machine.reset()

except:
    print('no update needed')
    pass

import main.start
