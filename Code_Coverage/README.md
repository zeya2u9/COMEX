# All utility scripts for the code coverqge

## autoacv1.py

This script automates the process of instrumenting the app and makes it ready for android code coverage using our modified version of https://github.com/pilgun/acvtool.git, it then uses the connected android device(MOTO G40 FUSION for our case) and using adb and acv tool installs the app, opens its main activity and then records the code coverage of the app. We can change the time parameter in both, this script and in smiler/smiler.py in the acvtool(in the stop function) for checking coverage for different time.

#### Note: We also would need to change the adb device ID in our script and our PATH respectively

## covereage2csv.py

This script takes output files from autoacv1.py, and using pandas, it extracts tables from the html output files, and makes a csv of all the packages' code coverage. For now this script takes seconds from 10-70, which can be changed

