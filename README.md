# COMEX
This repository contains "COMEX: Deeply Observing Application Behavior on Real Android Devices: code implementation accepted in CSET'24.

## COMEX Design Details

### DCoP
DCoP is the main data collection pipeline that analyzes individual APKs using the AXMod module. 

<div align = "center">
<img src="https://github.com/zeya2u9/COMEX/assets/108210209/92a10c2c-9f87-4ff9-8eb0-e99a8934d705" width="600" height="250">

</div>

### AXMoD
AXMoD works in two phases - (1) Setup phase, and (2) Analysis phase. 

#### Setup phase
In this phase we follow the above steps (shown in figure) to have a baseline device state. 

<img src="https://github.com/zeya2u9/COMEX/assets/108210209/7e22c81b-cfd1-4beb-b309-c848db5744c6" width="800" height="150">

#### Analysis phase
In this phase the APK under test is executed on the device and analysis data is pulled from it.

<img src="https://github.com/zeya2u9/COMEX/assets/108210209/9020254f-8801-4728-8eab-7dbd71c70380" width="800" height="150">

### Running the testbed
#### Requirements:
- Rooted device
- Connect device to the host PC using ADB. The DCoP module requires a host PC with connected devices for execution.
- Setting up a VM for each device. Since, 'monkeyrunner' does not support parallelism. Thus, to run monkeyrunner on mulitple devices simultaneously which are connected to a single host machine, we create multiple VMS and assign each device to a specific VM. 


### Modes of running the testbed

#### A. Testing of a single APK

##### Requirements
- Follow the pre-requisites to set up AXMoD.

##### Running the main script
- To execute the main script `raw_testbed.py`, located in the directory `<Path to COMEX>/COMEX/COMEX_AXMoD/raw_testbed.py`, you must provide a parameter specifying the full path to the APK file to be executed.

- An example testcase can be seen as follows:

```python
python3 raw_testbed.py <Path to COMEX>/COMEX/COMEX_AXMoD/apks/<APK name>
```

Running this script will generate analysis data in multiple folders such as netstat, stracelogs, etc. Refer to AXMoD for more details.

#### B. Completely automated testing of an APK database

##### Requirements:
- Follow the pre-requisites of AXMoD
- Follow the pre-requisites of DCoP

##### Running the main script
- To execute the main script `dynamic.py`, located in the directory `<Path to COMEX>/COMEX/COMEX_DCoP/dynamic.py>`.

- An example testcase can be seen as follows:

```python
python3 dynamic.py
```

Running this script will generate analysis data in VM's which can be transferred to some remote location as per requirement.
