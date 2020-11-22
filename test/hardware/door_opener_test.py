from pytest_mock import mocker
from test.stub_machine import *
import pytest, types, time

kippenstal = types.SimpleNamespace()

from src.app.hardware.door_opener import DoorOpener
from src.app.hardware.kippenstal_config import kippenstalConfig


@pytest.fixture(autouse=True)
def run_around_tests():
    yield
    known_pins.clear()
    kippenstalConfig.setDoorOpenerScheduleEnabled(True)

def test_doorOpener_doorClosedToggleDoor_openDoor(mocker):
    kippenstalConfig.setDoorOpenerScheduleEnabled(False)
    setUpKippenstal(8, 20)
    
    door_opener = DoorOpener(kippenstal)
    door_opener._isOpen = False
    door_opener.toggle()

    assert known_pins[0].vals == [-1, 0, 1]
    assert known_pins[1].vals == [-1, 0]

def test_doorOpener_doorOpenToggleDoor_closeDoor(mocker):
    kippenstalConfig.setDoorOpenerScheduleEnabled(False)
    setUpKippenstal(11, 20)
    
    door_opener = DoorOpener(kippenstal)
    door_opener._isOpen = True
    door_opener.toggle()

    assert known_pins[0].vals == [-1, 0]
    assert known_pins[1].vals == [-1, 0, 1]

def test_doorOpener_doorToggled1_noAction(mocker):
    setUpKippenstal(7, 20)
    
    door_opener = DoorOpener(kippenstal)
    door_opener._isOpen = False
    door_opener.toggle()

    door_opener.evaluate() #sets dark time
    kippenstal.currentTime = kippenstal.currentTime + 3601
    door_opener.evaluate() #it is still dark

    assert known_pins[0].vals == [-1, 0, 1]
    assert known_pins[1].vals == [-1, 0]

def test_doorOpener_doorToggled2_noAction(mocker):
    setUpKippenstal(11, 200)
    
    door_opener = DoorOpener(kippenstal)
    door_opener._isOpen = True
    door_opener.toggle()
    door_opener._isOpen = False #mimic timer

    door_opener.evaluate()

    assert known_pins[0].vals == [-1, 0]
    assert known_pins[1].vals == [-1, 0, 1]

def test_doorOpener_scheduleDisabledDoorClosedAndInsideTimeRange_noAction(mocker):
    kippenstalConfig.setDoorOpenerScheduleEnabled(False)
    setUpKippenstal(12, 20)
    
    door_opener = DoorOpener(kippenstal)
    door_opener._isOpen = False

    door_opener.evaluate()

    assert known_pins[0].lastVal() == -1
    assert known_pins[1].lastVal() == -1

def test_doorOpener_scheduleDisabledDoorOpenAndOutsideTimeRange_noAction(mocker):
    kippenstalConfig.setDoorOpenerScheduleEnabled(False)
    setUpKippenstal(3, 20)
    
    door_opener = DoorOpener(kippenstal)
    door_opener._isOpen = True

    door_opener.evaluate()

    assert known_pins[0].lastVal() == -1
    assert known_pins[1].lastVal() == -1

def test_doorOpener_doorClosedAndOutsideTimeRange_noAction(mocker):
    setUpKippenstal(3, 20)
    
    door_opener = DoorOpener(kippenstal)
    door_opener._isOpen = False

    door_opener.evaluate()

    assert known_pins[0].lastVal() == -1
    assert known_pins[1].lastVal() == -1

def test_doorOpener_doorOpenAndInsideTimeRange_noAction(mocker):
    setUpKippenstal(11, 20)
    
    door_opener = DoorOpener(kippenstal)
    door_opener._isOpen = True

    door_opener.evaluate()

    assert known_pins[0].lastVal() == -1
    assert known_pins[1].lastVal() == -1

def test_doorOpener_doorClosedAndInsideTimeRange_openDoor(mocker):
    setUpKippenstal(10, 20)
    
    door_opener = DoorOpener(kippenstal)
    door_opener._isOpen = False

    door_opener.evaluate()

    assert known_pins[0].vals == [-1, 0, 1]
    assert known_pins[1].vals == [-1, 0]

def test_doorOpener_doorOpenAndItStartsToGetDark_noAction(mocker):
    setUpKippenstal(18, 20)
    
    door_opener = DoorOpener(kippenstal)
    door_opener._isOpen = True

    door_opener.evaluate()

    assert known_pins[0].vals == [-1]
    assert known_pins[1].vals == [-1]

def test_doorOpener_doorOpenAndItMoreThan1HourDark_closeDoor(mocker):
    setUpKippenstal(18, 20)
    
    door_opener = DoorOpener(kippenstal)
    door_opener._isOpen = True
    door_opener.evaluate()

    kippenstal.currentTime = kippenstal.currentTime + 3601

    door_opener.evaluate()

    assert known_pins[0].vals == [-1, 0]
    assert known_pins[1].vals == [-1, 0, 1]


def setUpKippenstal(hour, lightSensorValue):
    kippenstal.currentTime = 1605476831.56942
    kippenstal.currentHour = str(hour)
    kippenstal.currentLightSensorValue = lightSensorValue
