from com.android.monkeyrunner import MonkeyDevice, MonkeyRunner
import sys

# Connect to the device
device = MonkeyRunner.waitForConnection()
device.wake()

#magisk coords
x = 900  # X-coordinate
y = 1350  # Y-coordinate
device.touch(x, y, MonkeyDevice.DOWN_AND_UP)
sys.exit(0)