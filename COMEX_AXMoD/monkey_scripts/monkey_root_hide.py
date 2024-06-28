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

# config denylist
app_x = 930  # X-coordinate
app_y = 860  # Y-coordinate
device.touch(app_x, app_y, MonkeyDevice.DOWN_AND_UP)
time.sleep(2)

# blocking all apps
app_x = 540  # X-coordinate
app_y = 375  # Y-coordinate
device.touch(app_x, app_y, MonkeyDevice.DOWN_AND_UP)
time.sleep(0.5)
app_x = 940  # X-coordinate
app_y = 375  # Y-coordinate
device.touch(app_x, app_y, MonkeyDevice.DOWN_AND_UP)
time.sleep(0.5)
app_x = 540  # X-coordinate
app_y = 375  # Y-coordinate
device.touch(app_x, app_y, MonkeyDevice.DOWN_AND_UP)
time.sleep(0.5)

app_x = 540  # X-coordinate
app_y = 550  # Y-coordinate
device.touch(app_x, app_y, MonkeyDevice.DOWN_AND_UP)
time.sleep(0.5)
app_x = 940  # X-coordinate
app_y = 550  # Y-coordinate
device.touch(app_x, app_y, MonkeyDevice.DOWN_AND_UP)
time.sleep(0.5)
app_x = 540  # X-coordinate
app_y = 550  # Y-coordinate
device.touch(app_x, app_y, MonkeyDevice.DOWN_AND_UP)
time.sleep(0.5)

app_x = 540  # X-coordinate
app_y = 725  # Y-coordinate
device.touch(app_x, app_y, MonkeyDevice.DOWN_AND_UP)
time.sleep(0.5)
app_x = 940  # X-coordinate
app_y = 725  # Y-coordinate
device.touch(app_x, app_y, MonkeyDevice.DOWN_AND_UP)
time.sleep(0.5)
app_x = 540  # X-coordinate
app_y = 725  # Y-coordinate
device.touch(app_x, app_y, MonkeyDevice.DOWN_AND_UP)
time.sleep(0.5)

os.system('adb shell input keyevent KEYCODE_BACK')
time.sleep(0.5)

os.system('adb shell am start -a android.intent.action.MAIN -c android.intent.category.HOME')
time.sleep(0.5)

sys.exit(0)