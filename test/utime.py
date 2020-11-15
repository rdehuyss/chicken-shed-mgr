from datetime import datetime
import time

def strftime(format, time):
    return datetime.now().strftime(format)

def localtime():
    return time.localtime()