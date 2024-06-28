from com.android.monkeyrunner import MonkeyDevice, MonkeyRunner
import sys
import time

# Connect to the device
device = MonkeyRunner.waitForConnection()
device.wake()

#APP START
x = 950  # X-coordinate
y = 1850  # Y-coordinate
device.touch(x, y, MonkeyDevice.DOWN_AND_UP)
time.sleep(2)

#3dot
x = 1025  # X-coordinate
y = 205  # Y-coordinate
device.touch(x, y, MonkeyDevice.DOWN_AND_UP)
time.sleep(2)

#play protect
x = 830  # X-coordinate
y = 435  # Y-coordinate
device.touch(x, y, MonkeyDevice.DOWN_AND_UP)
time.sleep(2)

#settings
x = 1025  # X-coordinate
y = 160  # Y-coordinate
device.touch(x, y, MonkeyDevice.DOWN_AND_UP)
time.sleep(2)

#toggle
x = 910  # X-coordinate
y = 515  # Y-coordinate
device.touch(x, y, MonkeyDevice.DOWN_AND_UP)
time.sleep(2)

#approve
x = 910  # X-coordinate
y = 1345  # Y-coordinate
device.touch(x, y, MonkeyDevice.DOWN_AND_UP)

sys.exit(0)