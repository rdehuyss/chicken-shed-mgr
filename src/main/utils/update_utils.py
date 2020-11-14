import main.ulogging as ulogging

try:
    with open('.updateRequested', "r") as updateRequested:
        ulogging.info('Update requested...')
        connectToWifi()
        updateTimeUsingNTP()
        otaUpdate()
        ulogging.info('Updates finished, will reboot')

    os.remove('.updateRequested')
    machine.reset()

except:
    ulogging.info('No update needed')
    pass


def connectToWifi():
    import utime, network, main.secrets as secrets
    from main.utils.httpclient import HttpClient
    ulogging.info('Connecting to WIFI')

    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)

    startTime = utime.time()
    while not sta_if.isconnected():
        if startTime + 45 < utime.time():
            break

        utime.sleep(2)
        sta_if.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)
    ulogging.info('Connected to WIFI')


def updateTimeUsingNTP():
    ulogging.info('Updating time...')
    import machine
    rtc = machine.RTC()
    rtc.ntp_sync(server="0.be.pool.ntp.org", tz="CET-1CEST,M3.5.0,M10.5.0/3")
    ulogging.info('Updated time...')


def otaUpdate():
    from .ota_updater import OTAUpdater
    otaUpdater = OTAUpdater('https://github.com/rdehuyss/chicken-shed-mgr')
    otaUpdater.download_update_if_available()