# COMEX_DCoP Module

This module automates the analysis of APK files using multiple virtual machines (VMs) connected to mobile phones. The system is designed to efficiently distribute APKs, execute analysis scripts on the VMs, and collect the resulting data.

## Directory Structure

- `~/COMEX/COMEX_DCoP/scripts/crash_resume/`
    - `counters.json`: Stores counters for analyzed benign and malware APKs.
    - Other files for crash recovery.

- `~/COMEX/COMEX_DCoP/metadata/`
    - CSV files with metadata for benign and malware APKs. Each CSV is named in the format `<year>_<family>.csv`.

- `~/COMEX/COMEX_DCoP/crash_resume/`
    - `benign_done.txt`: Tracks analyzed benign APKs.
    - `malware_done.txt`: Tracks analyzed malware APKs.

- `~/COMEX/COMEX_AXMoD/batterystats/`
    - Analysis results for APKs, stored as `<hash>-batterystats.csv`.

## How It Works

1. **Initialization**:
   - Load counters from `counters.json`.
   - Populate databases with APK metadata from CSV files in `~/COMEX/COMEX_DCoP/metadata/`.

2. **Task Dispatching**:
   - Separate dispatchers for benign and malware APKs:
     - `BenignTaskDispatcher`
     - `MalwareTaskDispatcher`
   - Dispatchers manage and assign tasks based on APK type, year, and malware family.

3. **Task Execution**:
   - `PhoneWorkerThread` handles the execution of analysis tasks on assigned VMs.
   - APKs are transferred from the server to the VMs using SCP.
   - The `raw_testbed.py` script is executed on the VMs to analyze the APKs.
   - Results are stored in `~/COMEX/COMEX_AXMoD/batterystats/`.

4. **Logging and Monitoring**:
   - Logs are printed to track the progress and state of dispatchers and worker threads.
   - Analysis results are updated in `counters.json`.

## Usage

### Restarting the Testbed

To restart the testbed from scratch:
1. Delete `counters.json`.
2. Clear `benign_done.txt` and `malware_done.txt`.

### Running the Script

Execute the main script to start the task dispatching and analysis process:
```bash
python3 dynamic.py
```
# Data Storage and Notes

## Data Storage

### Analysis Counters

- **Path**: `~/COMEX/COMEX_DCoP/scripts/crash_resume/counters.json`
- **Contents**: Stores counters for analyzed benign and malware APKs. The counters keep track of the number of APKs analyzed per year and per family.

### Done APKs

- **Path**: `~/COMEX/COMEX_DCoP/crash_resume/`
  - `benign_done.txt`: Tracks analyzed benign APKs.
  - `malware_done.txt`: Tracks analyzed malware APKs.
- **Contents**: Lists of APK hashes that have been analyzed, preventing duplicate analysis.

### APK Metadata

- **Path**: `~/COMEX/COMEX_DCoP/metadata/`
- **Contents**: CSV files containing metadata for benign and malware APKs, including hash values and paths. Each CSV is named in the format `<year>_<family>.csv`.

### Analysis Results

- **Path**: `~/COMEX/COMEX_AXMoD/batterystats/`
- **Contents**: CSV files containing the analysis results for each APK. The files are named `<hash>-batterystats.csv`.

## Notes

- Ensure that VM credentials and paths are correctly configured in the script.
- Adjust the `year_target` and `family_targets` as per the analysis requirements.
- Monitor the logs for any errors or issues during the analysis process.
- The system relies on SSH and SCP for file transfers. Ensure `sshpass` is installed and properly configured.
