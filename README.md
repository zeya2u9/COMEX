# COMEX
This repository contains "COMEX: Deeply Observing Application Behavior on Real Android Devices: code implementation accepted in CSET'24.

## COMEX Design Details

### DCoP
DCoP is the main data collection pipeline that analyzes individual APKs using the AXMod module. 

<div align = "center">
<img src="https://github.com/zeya2u9/COMEX/assets/108210209/f926f24a-b835-4050-99e0-42dbaea53034" width="600" height="250">
</div>

### AXMoD
AXMoD works in two phases - (1) Setup phase, and (2) Analysis phase. 

#### Setup phase
In this phase we follow the above steps (shown in figure) to have a baseline device state. 

<img src="https://github.com/zeya2u9/COMEX/assets/108210209/2647f53b-4382-4fcd-ac22-882133c37413" width="800" height="150">


#### Analysis phase
In this phase the APK under test is executed on the device and analysis data is pulled from it.

<img src="https://github.com/zeya2u9/COMEX/assets/108210209/a897c215-64ef-4716-8f0b-7c4d8ce8d0b5" width="800" height="150">
