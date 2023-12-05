# Image Acquisition Module
- This module manages data streams from the body camera and the dart camera
- `body_cam.py` and `dart_cam.py` are responsible for camera initialization, continuous data acquisition and data storage
- These scripts use the `sensorimotorkit/common/common_utils.py` script for trial management 
- The data is stored in the following format:
    - `sensorimotorkit/data/<date>/<trial_id>/<modality>/<body_cam/dart_cam>/<image_name>.png`