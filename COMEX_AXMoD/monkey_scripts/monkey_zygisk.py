from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
import sys
import time
import os


# Connect to the device
device = MonkeyRunner.waitForConnection()
device.wake()

# start_x = 500
# start_y = 1500  # Starting coordinates
# end_x = 500
# end_y = 500       # Ending coordinates

# # Simulate a swipe up
# device.drag((start_x, start_y), (end_x, end_y), 0, 100)
# time.sleep(0.5)

# # zygisk open
# app_x = 110  # X-coordinate
# app_y = 500  # Y-coordinate

# device.touch(app_x, app_y, MonkeyDevice.DOWN_AND_UP)
# time.sleep(2.75)

app_x = 150  # X-coordinate
app_y = 2300  # Y-coordinate
device.touch(app_x, app_y, MonkeyDevice.DOWN_AND_UP)
time.sleep(0.5)

# settings
app_x = 1025  # X-coordinate
app_y = 170  # Y-coordinate
device.touch(app_x, app_y, MonkeyDevice.DOWN_AND_UP)
time.sleep(0.5)

start_x = 500
start_y = 1500  # Starting coordinates
end_x = 500
end_y = 500       # Ending coordinates

# Simulate a swipe up
device.drag((start_x, start_y), (end_x, end_y), 0, 100)
time.sleep(1)

# for good measure
start_x = 500
start_y = 1500  # Starting coordinates
end_x = 500
end_y = 500       # Ending coordinates

# Simulate a swipe up
device.drag((start_x, start_y), (end_x, end_y), 0, 100)
time.sleep(1)


# zygisk module load
app_x = 950  # X-coordinate
app_y = 510  # Y-coordinate
device.touch(app_x, app_y, MonkeyDevice.DOWN_AND_UP)
time.sleep(1)

# enforce denylist
app_x = 930  # X-coordinate
app_y = 690  # Y-coordinate
device.touch(app_x, app_y, MonkeyDevice.DOWN_AND_UP)

sys.exit(0)