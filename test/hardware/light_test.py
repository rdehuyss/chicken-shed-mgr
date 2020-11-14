from pytest_mock import mocker
from test.stub_machine import *
import pytest, types

kippenstal = types.SimpleNamespace()

from src.hardware.light import Light


@pytest.fixture(autouse=True)
def run_around_tests():
    yield
    known_pins.clear()
    

def test_lightOffAndOutsideTimeRange_noAction(mocker):
    kippenstal.currentHour = 3
    
    light = Light(kippenstal)

    light.evaluate()

    assert known_pins[0].lastVal() == -1

def test_lightOnAndOutsideTimeRange_noAction(mocker):
    kippenstal.currentHour = 3
    kippenstal.currentLightSensorValue = 20
    
    light = Light(kippenstal)
    light.value = True

    light.evaluate()

    assert known_pins[0].lastVal() == 0
