from pytest_mock import mocker
from test.stub_machine import *
import pytest, types, time

kippenstal = types.SimpleNamespace()

from src.app.hardware.light import Light
from src.app.hardware.kippenstal_config import kippenstalConfig


@pytest.fixture(autouse=True)
def run_around_tests():
    yield
    known_pins.clear()
    kippenstalConfig.setLightScheduleEnabled(True)
    

def test_lightOffAndLightScheduleDisabled_noAction(mocker):
    kippenstalConfig.setLightScheduleEnabled(False)
    setUpKippenstal(7, 20)
    
    light = Light(kippenstal)
    light.value = False

    light.evaluate()

    assert known_pins[0].lastVal() == -1

def test_lightOnAndLightScheduleDisabled_noAction(mocker):
    kippenstalConfig.setLightScheduleEnabled(False)
    setUpKippenstal(3, 20)
    
    light = Light(kippenstal)
    light.value = True

    light.evaluate()

    assert known_pins[0].lastVal() == -1

def test_lightOffAndOutsideTimeRange_noAction(mocker):
    setUpKippenstal(3, 20)
    
    light = Light(kippenstal)

    light.evaluate()

    assert known_pins[0].lastVal() == -1

def test_lightOnAndOutsideTimeRange_turnOffLight(mocker):
    setUpKippenstal(3, 20)
    
    light = Light(kippenstal)
    light.value = True

    light.evaluate()

    assert known_pins[0].lastVal() == 0

def test_lightOffAndInsideTimeRangeAndDark_turnOnLight(mocker):
    setUpKippenstal(6, 20)
    
    light = Light(kippenstal)
    light.value = False

    light.evaluate()

    assert known_pins[0].lastVal() == 1


def test_lightOffAndInsideTimeRangeAndBright_turnOnLight(mocker):
    setUpKippenstal(6, 200)
    
    light = Light(kippenstal)
    light.value = False

    light.evaluate()

    assert known_pins[0].lastVal() == -1

def test_lightOnAndInsideTimeRangeAndBright_turnOnLight(mocker):
    setUpKippenstal(6, 200)
    
    light = Light(kippenstal)
    light.value = True

    light.evaluate()

    assert known_pins[0].lastVal() == 0

def test_lightOnToggle_turnOffLight(mocker):
    setUpKippenstal(6, 200)
    
    light = Light(kippenstal)
    light.value = True

    light.toggle()

    assert known_pins[0].lastVal() == 0

def test_lightOffToggle_turnOnLight(mocker):
    setUpKippenstal(6, 200)
    
    light = Light(kippenstal)
    light.value = False

    light.toggle()

    assert known_pins[0].lastVal() == 1

def test_lightOffToggleTurnOnLight_thenEvaluate_KeepsLightOn(mocker):
    setUpKippenstal(16, 200)
    
    light = Light(kippenstal)
    light.value = False

    light.toggle()

    light.evaluate()

    assert known_pins[0].lastVal() == 1

def test_lightOffToggleTurnOnLight_thenEvaluate1HourLaterWithEnoughLight_turnOffLight(mocker):
    setUpKippenstal(16, 200)
    
    light = Light(kippenstal)
    light.value = False

    light.toggle()

    kippenstal.currentTime = kippenstal.currentTime + 3601

    light.evaluate()

    assert known_pins[0].lastVal() == 0


def setUpKippenstal(hour, lightSensorValue):
    kippenstal.currentTime = 1605476831.56942
    kippenstal.currentHour = str(hour)
    kippenstal.currentLightSensorValue = lightSensorValue
