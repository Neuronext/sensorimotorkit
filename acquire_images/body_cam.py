from rotpy.camera import CameraList
import cv2
import numpy as np
import time
import os
import pickle
from common_utils import get_folder_count
from rotpy.system import SpinSystem
from rotpy.camera import CameraList

system = SpinSystem()
cameras = CameraList.create_from_system(system, update_cams=True, update_interfaces=True)

def acquire_images_common(cam_index, date_folder, fourcc, frame_rate, barrier, cam_folder, acquire_time):
    print(f"Starting body camera {cam_index+1}")
    camera = cameras.create_camera_by_index(cam_index)
    camera.init_cam()

    resolution = (camera.camera_nodes.Height.get_node_value(), camera.camera_nodes.Width.get_node_value()) # probably can be hardcoded
    print(resolution)
    cam_folder = f"body_tracking/camera_{cam_index+1}"
    index = (get_folder_count(os.path.join(date_folder, cam_folder, 'raw')) -1) if get_folder_count(os.path.join(date_folder, cam_folder, 'raw')) > 0 else 0 
    # ^ this could potientially be a bug if we do not add the if else statement

    camera.begin_acquisition()

    start_time = time.time()
    while time.time() - start_time < acquire_time:
        # barrier.wait()
        fps_start = time.time()
        image_count = int((time.time() - start_time) * frame_rate)
        image = camera.get_next_image()
        raw_data = image.get_image_data()

        # frame = np.array(image.get_image_data()).reshape(resolution)
        # frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        with open(f"{date_folder}/{cam_folder}/raw/{index}/frame_{image_count}_{cam_index+1}.pkl", "wb") as f:
            pickle.dump(raw_data, f)
        image.release()

        
        # try:
        #     cv2.imwrite(f"{date_folder}/{cam_folder}/raw/{index}/frame_{image_count}_{cam_index+1}.png", frame)
        # except Exception:
        #     break

        fps_end = time.time()
        fps = 1 / (fps_end - fps_start)
        print(f"Body {cam_index+1} FPS: {fps}")

        if cv2.waitKey(1) & 0xFF == 27:
            break

    camera.end_acquisition()
    camera.deinit_cam()
    camera.release()


