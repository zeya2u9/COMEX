from com.android.monkeyrunner import MonkeyDevice, MonkeyRunner
import time
import sys

# Connect to the device
device = MonkeyRunner.waitForConnection()
device.wake()

#1
x = 750  # X-coordinate
y = 1375  # Y-coordinate
device.touch(x, y, MonkeyDevice.DOWN_AND_UP)
time.sleep(1)

sys.exit(0)