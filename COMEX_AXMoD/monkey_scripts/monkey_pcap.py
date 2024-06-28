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
time.sleep(2)

#2
x = 925  # X-coordinate
y = 1440  # Y-coordinate
device.touch(x, y, MonkeyDevice.DOWN_AND_UP)
time.sleep(2)

# device = MonkeyRunner.waitForConnection()
# device.wake()

# #3
# x = 910  # X-coordinate
# y = 1515  # Y-coordinate
# device.touch(x, y, MonkeyDevice.DOWN_AND_UP)
# time.sleep(2)

sys.exit(0)

