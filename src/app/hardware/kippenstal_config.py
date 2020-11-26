import ujson

class KippenstalConfig:

    def __init__(self):
        self.__loadConfig()

    def getLightRelay(self):
        return self._config_data['light']['relay']

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

    def getLightFromHour(self):
        return self._config_data['light']['from_hour']

    def setLightFromHour(self, from_hour:int):
        if from_hour != self.getLightFromHour():
            self._config_data['light']['from_hour'] = from_hour
            self.__save_config()

    def getLightToHour(self):
        return self._config_data['light']['to_hour']

    def setLightToHour(self, to_hour:int):
        if to_hour != self.getLightToHour():
            self._config_data['light']['to_hour'] = to_hour
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
