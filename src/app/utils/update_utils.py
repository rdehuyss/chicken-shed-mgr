import app.ulogging as ulogging


class UpdateUtils:

    @staticmethod
    def updateIfNecessary():
        import machine, os
        try:
            with open('.updateRequested', "r") as updateRequested:
                pass

            try:
                os.remove('.updateRequested')
                ulogging.info('Update requested...')
                UpdateUtils._connectToWifi()
                UpdateUtils._updateTimeUsingNTP()
                UpdateUtils._otaUpdate()
                UpdateUtils._sendLogsToGithubGist()
                ulogging.info('Updates finished, will reboot')
            except BaseException as error:
                print(error)
                ulogging.error('Error updating: '+ str(error))
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
        import machine, utime
        from ..hardware.components.ds3231 import DS3231
        rtc = machine.RTC()
        rtc.ntp_sync(server="0.be.pool.ntp.org", tz="CET-1CEST-2,M3.5.0/02:00:00,M10.5.0/03:00:00")
        ds3231 = DS3231(machine.I2C(freq=400000, sda=21, scl=22))
        ds3231.save_time()
        ulogging.info("Updated time to {}".format(utime.strftime('%H:%M:%S', utime.localtime())))

    @staticmethod
    def _otaUpdate():
        ulogging.info('Checking for Updates...')
        from .ota_updater import OTAUpdater
        otaUpdater = OTAUpdater('https://github.com/rdehuyss/chicken-shed-mgr', github_src_dir='src', main_dir='app', secrets_file="secrets.py")
        otaUpdater.install_update_if_available()
        del(otaUpdater)
    
    @staticmethod
    def _sendLogsToGithubGist():
        import os
        if not 'logs.log' in os.listdir():
            return

        ulogging.info('Sending logs to GitHub Gist...')
        import app.secrets as secrets
        from .ota_logger import OTALogger
        o = OTALogger(secrets.GIST_ID, secrets.GIST_ACCESS_TOKEN)
        succeeded = o.log_to_gist('logs.log')
        if succeeded:
            ulogging.info('Sending logs to GitHub Gist succeeded...') 
            os.remove('logs.log')
        else:
            ulogging.warn('Sending logs to GitHub Gist failed...') 


UpdateUtils.updateIfNecessary()