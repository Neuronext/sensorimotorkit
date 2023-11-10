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
    cam_folder_for_trial = trial_path + Paths.DARTBOARD_RAW_PATH

    start_time = time.time()
    while time.time() - start_time < acquire_time:
        ret, frame = cap.read()
        if not ret:
            print("Failed to acquire image from Dart camera.")
            break
        image_count = int((time.time() - start_time) * frame_rate)
        try:
            cv2.imwrite(f"{cam_folder_for_trial}/frame_{image_count}_{cam_index+1}.png", frame)
        except Exception:
            break
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
