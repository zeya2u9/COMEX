from com.android.monkeyrunner import MonkeyDevice, MonkeyRunner
import sys

# Connect to the device
device = MonkeyRunner.waitForConnection()
device.wake()

#magisk coords
x = 739  # X-coordinate
y = 1502  # Y-coordinate
device.touch(x, y, MonkeyDevice.DOWN_AND_UP)
sys.exit(0)