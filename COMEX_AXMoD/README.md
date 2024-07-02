# APK Analysis Testbed

This repository contains a Python script `raw_testbed.py` designed to collect analysis data for an APK by running it on a device. It generates various types of data organized into folders such as `stracelogs`, `perfetto_traces`, `netstat`, `batterystat`, `lsof`, `pcaps`, etc. The script requires the use of `monkeyrunner` and `adb`.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Tools and Scripts](#tools-and-scripts)
- [Folder Structure](#folder-structure)

## Requirements

- Python 3.x
- Android Debug Bridge (adb)
- MonkeyRunner

## Installation

1. Clone this repository:
    ```sh
    git clone https://github.com/zeya2u9/COMEX.git
    cd COMEX_AXMoD
    ```
3. Ensure `adb` and `monkeyrunner` are installed and added to your system's PATH.

## Usage

1. Connect your Android device to your computer via USB and ensure USB debugging is enabled.

2. Run the `raw_testbed.py` script:
    ```sh
    python raw_testbed.py <path_to_apk>
    ```

3. The script will collect various types of data and save them in respective folders.

## Tools and Scripts

- **Monkeyrunner**: Used to control the device and interact with the APK.
- **ADB**: Used to communicate with the Android device.
- **Magisk**: Tool for rooting the device.
- **Pcapdroid**: App used to capture network data of a specific APK.
- **Strace**: Tool for capturing system calls.

## Folder Structure

- **raw_testbed.py**: Main script to run the analysis.
- **monkey_scripts/**: Contains all the Monkey and MonkeyRunner scripts used in the testbed.
- **andro_essentials/**: Contains essential tools required for the testbed, such as:
  - **Magisk**: Used to root the device.
  - **Pcapdroid**: Used to capture network data of a specific APK.
- **andro_bins/**: Contains the `strace` binary required to capture system calls for the specific APK.
- **apkinfo/**: Contains text files saved as `APK's hash.txt` which include the package name of the APK.
- **andro_bins/**: Contains the `strace` binary required to capture system calls for the specific APK.
- **apkinfo/**: Contains text files saved as `APK's hash.txt` which include the package name of the APK.
- **stracelogs/**: Contains system call logs.
- **perfetto_traces/**: Contains Perfetto traces.
- **netstat/**: Contains network statistics.
- **batterystat/**: Contains battery usage statistics.
- **lsof/**: Contains list of open files.
- **pcaps/**: Contains packet captures.
