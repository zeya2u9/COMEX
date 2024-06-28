from com.android.monkeyrunner import MonkeyDevice, MonkeyRunner
import sys
import time

# Connect to the device
device = MonkeyRunner.waitForConnection()
device.wake()

#old version dialog ok
x = 910  # X-coordinate
y = 1380  # Y-coordinate
device.touch(x, y, MonkeyDevice.DOWN_AND_UP)

sys.exit(0)