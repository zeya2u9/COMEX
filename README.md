# COMEX
This repository contains the code implementation of paper titled "COMEX: Deeply Observing Application Behavior on Real Android Devices" accepted in Usenix CSET'24. COMEX is a testbed for dynamic analysis of android applications on real mobile devices. 

## COMEX Design Details

```diff
### @@D@@ata **Co**llection **P**ipeline
```
DCoP is the main data collection pipeline that analyzes individual APKs using the AXMod module. 

<div align = "center">
<img src="https://github.com/zeya2u9/COMEX/assets/108210209/9020254f-8801-4728-8eab-7dbd71c70380" width="600" height="250">

</div>

### **A**nalysis e**X**ecution **MoD**ule
AXMoD works in two phases - (1) Setup phase, and (2) Analysis phase. 

#### (1) Setup phase
In this phase we follow the steps (shown in figure) to have a baseline device state. 

<img src="https://github.com/zeya2u9/COMEX/assets/108210209/92a10c2c-9f87-4ff9-8eb0-e99a8934d705" width="800" height="200">

#### (2) Analysis phase
In this phase the APK under test is executed on the device and analysis data is pulled from it.

<img src="https://github.com/zeya2u9/COMEX/assets/108210209/7e22c81b-cfd1-4beb-b309-c848db5744c6" width="800" height="200">


### Running the testbed
#### Requirements:
- Rooted device.
- Connect device to the host PC using ADB. The DCoP module requires a host PC with connected devices for execution.
- Setting up a virtual machine for each device. ['Monkeyrunner'](https://developer.android.com/studio/test/monkeyrunner) does not support parallelism. Thus, to run monkeyrunner on mulitple devices simultaneously which are connected to a single host machine, we create multiple VMs and assign each device to a specific VM. 


### Modes of running the testbed

#### A. Testing of a single APK

##### Requirements
- Setup AXMoD (follow its [readme](https://github.com/zeya2u9/COMEX/blob/main/COMEX_AXMoD/README.md)).

##### Running the module
- To execute the module run `raw_testbed.py`, located in the directory `<Path to COMEX>/COMEX/COMEX_AXMoD/raw_testbed.py`. You must provide a parameter specifying the full path to the APK file to be executed.

- An example testcase can be seen as follows:

```python
python3 raw_testbed.py <Path to COMEX>/COMEX/COMEX_AXMoD/apks/<APK name>
```

Running this script will generate raw analysis data in multiple folders such as netstat, stracelogs, *etc*. Refer to AXMoD for more details on raw data.

#### B. Completely automated testing of an APK database

##### Requirements:
- Setup AXMoD (follow its [readme](https://github.com/zeya2u9/COMEX/blob/main/COMEX_AXMoD/README.md))
- Setup DCoP (follow its [readme](https://github.com/zeya2u9/COMEX/blob/main/COMEX_DCoP/README.md))

##### Running the modules
- To execute the module run `dynamic.py`, located in the directory `<Path to COMEX>/COMEX/COMEX_DCoP/dynamic.py>`.

- An example testcase can be seen as follows:

```python
python3 dynamic.py
```

Running this script will generate raw analysis data in VM's which can be transferred to some remote location as per requirement.
