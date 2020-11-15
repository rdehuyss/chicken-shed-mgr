from pytest_mock import mocker
from test.stub_machine import *
import pytest, types, time

kippenstal = types.SimpleNamespace()

from src.app.hardware.fence import Fence
from src.app.hardware.kippenstal_config import kippenstalConfig


@pytest.fixture(autouse=True)
def run_around_tests():
    yield
    known_pins.clear()
    kippenstalConfig.setFenceOnState('on')
    

def test_fenceOnAndFenceScheduleAlwaysOn_noAction(mocker):
    kippenstalConfig.setFenceOnState('on')
    setUpKippenstal()
    
    fence = Fence(kippenstal)
    fence.value = True

    fence.evaluate()

    assert known_pins[0].lastVal() == -1

def test_fenceOffAndFenceScheduleAlwaysOn_electrifyFence(mocker):
    kippenstalConfig.setFenceOnState('on')
    setUpKippenstal()
    
    fence = Fence(kippenstal)
    fence.value = False

    fence.evaluate()

    assert known_pins[0].lastVal() == 1

def test_fenceOnAndFenceScheduleAlwaysOff_turnFenceOff(mocker):
    kippenstalConfig.setFenceOnState('off')
    setUpKippenstal()
    
    fence = Fence(kippenstal)
    fence.value = True

    fence.evaluate()

    assert known_pins[0].lastVal() == 0

def test_fenceOffAndFenceScheduleAlwaysOff_noAction(mocker):
    kippenstalConfig.setFenceOnState('off')
    setUpKippenstal()
    
    fence = Fence(kippenstal)
    fence.value = False

    fence.evaluate()

    assert known_pins[0].lastVal() == -1

def test_fenceOffAndFenceScheduleWithDoor_DoorOpen_electrifyFence(mocker):
    kippenstalConfig.setFenceOnState('on when door open')
    setUpKippenstal(True)
    
    fence = Fence(kippenstal)
    fence.value = False

    fence.evaluate()

    assert known_pins[0].lastVal() == 1

def test_fenceOnAndFenceScheduleWithDoor_DoorClosed_turnFenceOff(mocker):
    kippenstalConfig.setFenceOnState('on when door open')
    setUpKippenstal(False)
    
    fence = Fence(kippenstal)
    fence.value = True

    fence.evaluate()

    assert known_pins[0].lastVal() == 0



def setUpKippenstal(doorOpen = False):
    doorOpener = DoorOpenerStub(doorOpen)
    kippenstal.doorOpener = doorOpener

class DoorOpenerStub:

    def __init__(self, isOpen):
        self._isOpen = isOpen

    def isOpen(self):
        return self._isOpen

    def isClosed(self):
        return not self._isOpen