from rotpy.camera import CameraList
import cv2
import numpy as np
import time
import os
import pickle
from rotpy.system import SpinSystem
from rotpy.camera import CameraList
from common.constants import Paths

system = SpinSystem()
cameras = CameraList.create_from_system(system, update_cams=True, update_interfaces=True)

def acquire_images_common(cam_index, trial_path, fourcc, frame_rate, barrier, cam_folder, acquire_time):
    
    print(f"Starting body camera {cam_index}")
    camera = cameras.create_camera_by_index(cam_index)
    camera.init_cam()

    resolution = (camera.camera_nodes.Height.get_node_value(), camera.camera_nodes.Width.get_node_value()) # probably can be hardcoded
    print(f"Resolution of camera {cam_index}: {resolution}")
    #         raw_path = os.path.normpath(os.path.join(trial_path, path))
    cam_path = Paths.BODY_LEFT_RAW_PATH if cam_index == 0 else Paths.BODY_RIGHT_RAW_PATH
    cam_folder_for_trial = os.path.normpath(os.path.join(trial_path, cam_path))

    print(f"Saving images of camera {cam_index} to {cam_folder_for_trial}")
    camera.begin_acquisition()
    start_time = time.time()

    while time.time() - start_time < acquire_time:

        image_count = int((time.time() - start_time) * frame_rate)
        image = camera.get_next_image()
        raw_data = image.get_image_data()
        with open(f"{cam_folder_for_trial}/frame_{image_count}_{cam_index+1}.pkl", "wb") as f:
            pickle.dump(raw_data, f)
        image.release()
        if cv2.waitKey(1) & 0xFF == 27:
            break

    camera.end_acquisition()
    camera.deinit_cam()
    camera.release()


