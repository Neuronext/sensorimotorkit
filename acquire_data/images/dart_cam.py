import cv2
import time
import os
from common.constants import Paths

def acquire_dart_images(cam_index, trial_path, fourcc, frame_rate, barrier, cam_folder, acquire_time):
    print(f"Starting dart camera {cam_index+1}")
    cap = cv2.VideoCapture(cam_index)
    ret, frame = cap.read()
    if not ret:
        print("Failed to open Dart camera.")
        return

    resolution = frame.shape[:2]
    cam_folder_for_trial = os.path.normpath(os.path.join(trial_path, cam_folder))


    print(f"Dart camera {cam_index}, resolution: {resolution}, frame rate: {frame_rate}, cam_folder: {cam_folder_for_trial}")

    start_time = time.time()
    image_dump = []

    while time.time() - start_time < acquire_time:
        ret, frame = cap.read()
        if not ret:
            print("Failed to acquire image from Dart camera.")
            break
        
        timestamp = time.time()
        image_dump.append((timestamp, frame))

        if cv2.waitKey(1) & 0xFF == 27:
            break
    
    print(f"Saving images from dart camera {cam_index+1} to {cam_folder_for_trial}")
    for idx, (timestamp, frame) in enumerate(image_dump):
        cv2.imwrite(f"{cam_folder_for_trial}/frame_{idx}_{timestamp:.6f}.png", frame)

    cap.release()
