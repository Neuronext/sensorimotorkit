# Sensorimotor Kit
SensorimotorKit is a versatile toolbox designed to facilitate the recording and integration of various sensory data streams. It serves as an efficient link between the diverse input modalities and their respective output spaces.

## System specifications
- RAM: Minimum 32 GB
- Operating System: 64-bit Windows
- Storage: Minimum 250 GB
- Input Port Requirements: Cyton board, USB 3.0, Bluetooth

## Set up
We recommend using [Conda](https://docs.conda.io/en/latest/) to setup a dedicated environment for SensorimotorKit-related tasks.

- In order to install Conda follow the steps in the documentation below
    - [Windows](https://conda.io/projects/conda/en/latest/user-guide/install/windows.html)
    - [Mac](https://docs.conda.io/projects/conda/en/latest/user-guide/install/macos.html)
- Setup Conda environment with Python 3.10, here we have named it 'smk' for sensorimotorkit
    - `conda create -n smk -y python=3.10`
    - `conda activate smk`
- Clone SensorimotorKit and install dependencies
    - `git clone -b develop https://github.com/Neuronext/sensorimotorkit.git`
    - `cd sensorimotorkit`
    - `pip install -r requirements.txt`
- Run the main script to record data
    - `python main.py`

## Structure of the Kit
- The GUI module is located under `sensorimotorkit/gui`. It is responsible for collecting metadata from the user and starting the data acquisition module. The GUI can be invoked by running the main script `sensorimotorkit/main_gui.py`
- The data acquisition module can be found under `sensorimotorkit/acquire_data`
- Constants, utilities and configurations are stored under `sensorimotorkit/common`
- Post data acquisition we apply feature extraction, using the module `sensorimotorkit/feature_extraction`

## Data
- Data is stored under `sensorimotorkit/data`
- Data is stored in the following format:
    - `sensorimotorkit/data/<date>/<trial_id>/<modality>/<file_name>.csv`
    - `sensorimotorkit/data/<date>/<trial_id>/<modality>/<raw>/frame_<timestamp>.png`
- Here the `modality` includes eeg, emg, glove, eyes, body camera and dart cameras.

## Flow of the program
- The main script `sensorimotorkit/main.py` is the entry point of the program
- The main script invokes the data acquisition module `sensorimotorkit/acquire_data`
- The data acquisition module invokes the common module `sensorimotorkit/common` for utility functions and constants
- The data acquisition module writes the data to the disk and returns success/failure flags to the main script
- The main script invokes the feature extraction module `sensorimotorkit/feature_extraction` to convert the images to tracked images

## Tracking
- We use [Google Mediapipe](https://developers.google.com/mediapipe) for tracking
- We simply infer the landmarks from mediapipe for our feature extraction
- Tracking aims to infer 33 landmarks from the images which are then overlayed on the image and stored as `sensorimotorkit/data/<date>/<trial_id>/<modality>/body_<left/right>/processed/<tracked_image>.png`
