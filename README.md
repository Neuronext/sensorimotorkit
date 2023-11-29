# Sensorimotor Kit

## Set up
- In order to install conda follow the steps in the documentation below
    - [Windows](https://conda.io/projects/conda/en/latest/user-guide/install/windows.html)
    - [Mac](https://docs.conda.io/projects/conda/en/latest/user-guide/install/macos.html)
- Setup python 3.10 environment using conda, here we have named it 'smk' for sensorimotorkit
    - `conda create -n smk -y python=3.10`
    - `conda activate smk`
- Clone sensorimotorkit and install dependencies
    - `git clone -b develop https://github.com/Neuronext/sensorimotorkit.git`
    - `cd sensorimotorkit`
    - `pip install -r requirements.txt`
- Run the main script to record data
    - `python main.py`

## Structure of the Kit
- The main script is `sensorimotorkit/main.py`
- The data acquisition module can be found under `sensorimotorkit/data_acquisition`
- Utilities are stored under `sensorimotorkit/common`
- Constants and configurations are stored under `sensorimotorkit/common/constants.py`

## Data
- Data is stored under `sensorimotorkit/data`
- Data is stored in the following format:
    - `sensorimotorkit/data/<subject_id>/<session_id>/<trial_id>/<trial_id>.csv`
    - `sensorimotorkit/data/<subject_id>/<session_id>/<trial_id>/<trial_id>.mp4`


## Flow of the program
- The main script `sensorimotorkit/main.py` is the entry point of the program
- The main script invokes the data acquisition module `sensorimotorkit/data_acquisition`
- The data acquisition module invokes the common module `sensorimotorkit/common` for utility functions and constants
- The data acquisition module writes the data to the disk and returns success/failure flags to the main script
- The main script invokes the post processing module `sensorimotorkit/post_processing` to convert the images to tracked images

## Tracking
- We use [Google Mediapipe](https://developers.google.com/mediapipe) for tracking
- We just infer the landmarks from mediapipe for our feature extraction
- Tracking aims to infer 36 landmarks from the images which are cut down due to positioning, angle, occlusion, etc.
