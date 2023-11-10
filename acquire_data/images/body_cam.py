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

    resolution = (camera.camera_nodes.Height.get_node_value(), camera.camera_nodes.Width.get_node_value()) #TODO probably can be hardcoded, or should be in constants file

    cam_folder_for_trial = os.path.normpath(os.path.join(trial_path, cam_folder))
    print(f"Camera {cam_index}, resolution: {resolution}, frame rate: {frame_rate}, cam_folder: {cam_folder_for_trial}")

    camera.begin_acquisition()
    start_time = time.time()

    image_dump = []

    while time.time() - start_time < acquire_time:

        image = camera.get_next_image()
        raw_data = image.get_image_data()
        
        timestamp = time.time()
        image_dump.append((timestamp, raw_data))

        image.release()
        
        if cv2.waitKey(1) & 0xFF == 27:
            break
    
    print(f"Saving images of camera {cam_index} to {cam_folder_for_trial}")
    for idx, (timestamp, raw_data) in enumerate(image_dump): #TODO find a scalable way to save images
        frame = np.array(raw_data).reshape(resolution)
        #TODO add rotation based on camera - should not be hardcoded - ideally should be in the constants file
        cv2.imwrite(f"{cam_folder_for_trial}/frame_{idx}_{timestamp:.6f}.png", frame)

    camera.end_acquisition()
    camera.deinit_cam()
    camera.release()


