from rotpy.camera import CameraList
import cv2
import numpy as np
import time
import os
from rotpy.system import SpinSystem
from rotpy.camera import CameraList
# from camera import SpinViewCamera, OpenCVCamera
from common.constants import MetadataConstants

system = SpinSystem()
cameras = CameraList.create_from_system(system, update_cams=True, update_interfaces=True)


class SpinViewCamera():
    def __init__(self, cam_index):
        self.cam_index = cam_index
        self.camera = None
        
    def init_cam(self):
        self.camera = cameras.create_camera_by_index(self.cam_index)
        self.camera.init_cam()

    def get_next_image(self):
        return self.camera.get_next_image()

    def end_acquisition(self):
        self.camera.end_acquisition()

    def deinit_cam(self):
        self.camera.deinit_cam()

    def get_camera_resolution(self):
        return (self.camera.camera_nodes.Height.get_node_value(), self.camera.camera_nodes.Width.get_node_value())


class OpenCVCamera():
    def __init__(self, cam_index):
        self.cam_index = cam_index
        self.camera = None

    def init_cam(self):
        self.camera = cv2.VideoCapture(self.cam_index)

    def get_next_image(self):
        ret, frame = self.camera.read()
        if not ret:
            raise RuntimeError("Failed to read from camera.")
        return frame

    def end_acquisition(self):
        if self.camera:
            self.camera.release()

    def deinit_cam(self):
        pass

    def get_camera_resolution(self):
        return (int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)))


def create_camera(camera_type, cam_index):
    if camera_type == "spinview":
        return SpinViewCamera(cam_index)
    elif camera_type == "opencv":
        return OpenCVCamera(cam_index)
    else:
        raise ValueError("Unknown camera type")
    
# def get_camera_resolution(camera, camera_type, cam_index):
#     if camera_type == "spinview":
#         resolution = (camera.camera_nodes.Height.get_node_value(), camera.camera_nodes.Width.get_node_value())
#         camera.deinit_cam()
#         return resolution
#     elif camera_type == "opencv":
#         camera = cv2.VideoCapture(cam_index)
#         resolution = (int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)))
#         camera.release()
#         return resolution
#     else:
#         raise ValueError("Unknown camera type")


def acquire_images_common(cam_index, trial_path, fourcc, frame_rate, barrier, cam_folder, acquire_time):
    
    print(f"Starting body camera {cam_index}")
    # camera = cameras.create_camera_by_index(cam_index)
    camera = create_camera(camera_type=MetadataConstants.CAMERA, cam_index=cam_index)
    camera.init_cam()

    resolution = camera.get_camera_resolution()
    
    # (camera.camera_nodes.Height.get_node_value(), camera.camera_nodes.Width.get_node_value()) #TODO probably can be hardcoded, or should be in constants file

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
    
    print(f"Saving images of body camera {cam_index} to {cam_folder_for_trial}")
    for idx, (timestamp, raw_data) in enumerate(image_dump): #TODO find a scalable way to save images
        frame = np.array(raw_data).reshape(resolution)
        if cam_index == 0:
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        else:
            frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        #TODO add rotation based on camera - should not be hardcoded - ideally should be in the constants file
        cv2.imwrite(f"{cam_folder_for_trial}/frame_{idx}_{timestamp:.6f}.png", frame)

    camera.end_acquisition()
    camera.deinit_cam()
    camera.release()


