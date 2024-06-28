from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
import sys
import time
import os

device = MonkeyRunner.waitForConnection()
device.wake()

app_x = 350  # X-coordinate
app_y = 2300  # Y-coordinate
device.touch(app_x, app_y, MonkeyDevice.DOWN_AND_UP)
time.sleep(0.5)

app_x = 900  # X-coordinate
app_y = 350 # Y-coordinate
device.touch(app_x, app_y, MonkeyDevice.DOWN_AND_UP)
time.sleep(0.5)








