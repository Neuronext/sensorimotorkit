import cv2
import time
import os
from common_utils import get_folder_count

def acquire_dart_images(cam_index, date_folder, fourcc, frame_rate, barrier, cam_folder, acquire_time):
    print(f"Starting dart camera {cam_index+1}")
    cap = cv2.VideoCapture(cam_index)
    ret, frame = cap.read()
    if not ret:
        print("Failed to open Dart camera.")
        return

    frame_rate = 30  # Dart camera
    resolution = frame.shape[:2]

    index = (get_folder_count(os.path.join(date_folder, cam_folder, 'raw')) - 1) if get_folder_count(os.path.join(date_folder, cam_folder, 'raw')) > 0 else 0

    start_time = time.time()
    while time.time() - start_time < acquire_time:
        # barrier.wait()
        fps_start = time.time()
        ret, frame = cap.read()
        if not ret:
            print("Failed to acquire image from Dart camera.")
            break
        
        image_count = int((time.time() - start_time) * frame_rate)
        try:
            cv2.imwrite(f"{date_folder}/{cam_folder}/raw/{index}/frame_{image_count}_{cam_index+1}.png", frame)
        except Exception:
            break

        fps_end = time.time()
        fps = 1 / (fps_end - fps_start)
        # print(f"Dart {cam_index+1} FPS: {fps}")
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
