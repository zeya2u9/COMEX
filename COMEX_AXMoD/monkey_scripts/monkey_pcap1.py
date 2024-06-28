from com.android.monkeyrunner import MonkeyDevice, MonkeyRunner
import time
import sys

device = MonkeyRunner.waitForConnection()
device.wake()

print("Second time connection established")

x = 910  # X-coordinate
y = 1515  # Y-coordinate
device.touch(x, y, MonkeyDevice.DOWN_AND_UP)
time.sleep(2)

print("tap done")

sys.exit(0)