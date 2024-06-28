from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
import sys
import time


# Connect to the device
device = MonkeyRunner.waitForConnection()
device.wake()

# # Define the starting and ending coordinates for the swipe
start_x = 500
start_y = 1500  # Starting coordinates
end_x = 500
end_y = 500       # Ending coordinates

# # Simulate a swipe up
device.drag((start_x, start_y), (end_x, end_y), 0, 100)

time.sleep(0.5)

# Now, define the coordinates where you want to click on the app
app_x = 600  # X-coordinate
app_y = 500  # Y-coordinate

# Perform a touch at the specified coordinates to click on the app
device.touch(app_x, app_y, MonkeyDevice.DOWN_AND_UP)
sys.exit(0)
