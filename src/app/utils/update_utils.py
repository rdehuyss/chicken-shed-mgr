import app.ulogging as ulogging


class UpdateUtils:

    @staticmethod
    def updateIfNecessary():
        import machine, os
        try:
            with open('.updateRequested', "r") as updateRequested:
                try:
                    ulogging.info('Update requested...')
                    UpdateUtils._connectToWifi()
                    UpdateUtils._updateTimeUsingNTP()
                    UpdateUtils._otaUpdate()
                    ulogging.info('Updates finished, will reboot')
                except BaseException as error:
                    print(error)
                    ulogging.error('Error updating: '+ str(error))

            os.remove('.updateRequested')
            machine.reset()


        except BaseException as error:
            print(error)
            ulogging.info('No update needed')
            pass

    @staticmethod
    def _connectToWifi():
        import utime, network, app.secrets as secrets
        from app.utils.httpclient import HttpClient
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

    @staticmethod
    def _updateTimeUsingNTP():
        ulogging.info('Updating time...')
        import machine
        rtc = machine.RTC()
        rtc.ntp_sync(server="0.be.pool.ntp.org", tz="CET-1CEST,M3.5.0,M10.5.0/3")
        ulogging.info('Updated time...')

    @staticmethod
    def _otaUpdate():
        from .ota_updater import OTAUpdater
        otaUpdater = OTAUpdater('https://github.com/rdehuyss/chicken-shed-mgr', github_src_dir='src', main_dir='app', secrets_file="secrets.py")
        otaUpdater.install_update_if_available()

UpdateUtils.updateIfNecessary()