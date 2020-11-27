import ujson

class KippenstalConfig:

    def __init__(self):
        self.__loadConfig()

    def getLight1Relay(self):
        return self._config_data['light']['light1']['relay']
    
    def getLight2Relay(self):
        return self._config_data['light']['light2']['relay']

    def isLightScheduleEnabled(self):
        return self._config_data['light']['schedule_enabled']

    def setLightScheduleEnabled(self, value:bool):
        if value != self.isLightScheduleEnabled():
            self._config_data['light']['schedule_enabled'] = value
            self.__save_config()

    def getLightThreshold(self):
        return self._config_data['light']['threshold']

    def setLightThreshold(self, value:int):
        if value != self.getLightThreshold():
            self._config_data['light']['threshold'] = value
            self.__save_config()

    def getLight1From(self) -> str:
        return self._config_data['light']['light1']['from']

    def setLight1From(self, fromTime:str):
        if fromTime != self.getLight1From():
            self._config_data['light']['light1']['from'] = fromTime
            self.__save_config()

    def getLight1To(self) -> str:
        return self._config_data['light']['light1']['to']

    def setLight1To(self, toTime:str):
        if toTime != self.getLight1To():
            self._config_data['light']['light1']['to'] = toTime
            self.__save_config()

    def getLight2From(self) -> str:
        return self._config_data['light']['light2']['from']

    def setLight2From(self, fromTime:str):
        if fromTime != self.getLight2From():
            self._config_data['light']['light2']['from'] = fromTime
            self.__save_config()

    def getLight2To(self) -> str:
        return self._config_data['light']['light2']['to']

    def setLight2To(self, toTime:str):
        if toTime != self.getLight2To():
            self._config_data['light']['light2']['to'] = toTime
            self.__save_config()

    def getFenceRelay(self):
        return self._config_data['fence']['relay']

    def getFenceOnState(self):
        return self._config_data['fence']['on_when']

    def setFenceOnState(self, on_when:str):
        if on_when != self.getFenceOnState():
            self._config_data['fence']['on_when'] = on_when
            self.__save_config()

    def getDoorOpenerOpenRelay(self):
        return self._config_data['door_opener']['open_relay']

    def getDoorOpenerCloseRelay(self):
        return self._config_data['door_opener']['close_relay']

    def isDoorOpenerScheduleEnabled(self):
        return self._config_data['door_opener']['schedule_enabled']

    def setDoorOpenerScheduleEnabled(self, value:bool):
        if value != self.isDoorOpenerScheduleEnabled():
            self._config_data['door_opener']['schedule_enabled'] = value
            self.__save_config()

    def getDoorOpenAtHour(self):
        return self._config_data['door_opener']['open_at_hour']

    def setDoorOpenAtHour(self, value:int):
        if value != self.getDoorOpenAtHour():
            self._config_data['door_opener']['open_at_hour'] = value
            self.__save_config()

    def getDoorCloseAtHour(self):
        return self._config_data['door_opener']['close_at_hour_after_sunset']

    def setDoorCloseAtHour(self, value:int):
        if value != self.getDoorOpenAtHour():
            self._config_data['door_opener']['close_at_hour_after_sunset'] = value
            self.__save_config()

    def __loadConfig(self):
        with open('config.json') as f:
            self._config_data = ujson.load(f)
            f.close()

    def __save_config(self):
        with open('config.json', 'w') as f:
            f.write(ujson.dumps(self._config_data))
            f.close()

kippenstalConfig = KippenstalConfig()
