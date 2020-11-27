import utime, os

CRITICAL = 50
ERROR    = 40
WARN  = 30
INFO     = 20
DEBUG    = 10
NOTSET   = 0

_level_dict = {
    CRITICAL: "CRIT",
    ERROR: "ERROR",
    WARN: "WARN",
    INFO: "INFO",
    DEBUG: "DEBUG",
}


class Logger:

    level = NOTSET
    handlers = []

    def __init__(self, name):
        self.name = name

    def _level_str(self, level):
        l = _level_dict.get(level)
        if l is not None:
            return l
        return "LVL%s" % level

    def setLevel(self, level):
        self.level = level

    def isEnabledFor(self, level):
        return level >= (self.level or _level)

    def log(self, level, msg, *args):
        if self.isEnabledFor(level):
            levelname = self._level_str(level)
            if args:
                msg = msg % args

            logMsg = ''
            if self.name == 'root':
                logMsg = "{} - {} - {}".format(utime.strftime('%Y-%m-%d %H:%M:%S', utime.localtime()), levelname, msg)
            else:
                logMsg = "{} - {}:{} - {}".format(utime.strftime('%Y-%m-%d %H:%M:%S', utime.localtime()), levelname, self.name, msg)
            
            print(logMsg)
            if 'logs.log' in os.listdir() and os.stat("logs.log")[6] > 64000:
                os.remove("logs.log")
            with open("logs.log", "a") as file_object:
                file_object.write(logMsg + "\n")

    def debug(self, msg, *args):
        self.log(DEBUG, msg, *args)

    def info(self, msg, *args):
        self.log(INFO, msg, *args)

    def warn(self, msg, *args):
        self.log(WARN, msg, *args)

    def error(self, msg, *args):
        self.log(ERROR, msg, *args)

    def critical(self, msg, *args):
        self.log(CRITICAL, msg, *args)

    def exc(self, e, msg, *args):
        self.log(ERROR, msg, *args)

_level = INFO
_loggers = {}

def getLogger(name="root"):
    if name in _loggers:
        return _loggers[name]
    l = Logger(name)
    _loggers[name] = l
    return l

def info(msg, *args):
    getLogger().info(msg, *args)

def debug(msg, *args):
    getLogger().debug(msg, *args)

def warn(msg, *args):
    getLogger().warn(msg, *args)

def error(msg, *args):
    getLogger().error(msg, *args)
