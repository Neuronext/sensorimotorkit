# GUI module
- This module contains code for altering the GUI 
- The constants are picked up from `common/constants.py`, the user can change these directly in the file. In particular the user can change the `MetadataConstants` to include/exclude modalities from the GUI and also change parameters like trails per batch, polling interval, sleep time etc.
- GUI takes some metadata parameters of the user like ID, handedness,age, gender etc.
- The user can select the data folder on the GUI, which when not selected is defaulted to `sensorimotorkit/data`