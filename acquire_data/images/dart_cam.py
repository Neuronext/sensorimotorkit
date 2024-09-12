import cv2
import os
import time
import simpleaudio as sa

def acquire_dart_images(cam_index, trial_path, fourcc, frame_rate, barrier, cam_folder, intervals):
    print(f"Starting dart camera {cam_index+1}")

    cap = cv2.VideoCapture(cam_index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    ret, frame = cap.read()
    if not ret:

        failed_path = 'C:/Users/Data acquisition/sensorimotorkit/assets/audio/Failed.wav'
        failed_wave = sa.WaveObject.from_wave_file(failed_path)
        failed_play = failed_wave.play()
        failed_play.wait_done()
        #capture_frame()
        print("Failed to open Dart camera.")
        return

    resolution = frame.shape[:2]
    cam_folder_for_trial = os.path.normpath(os.path.join(trial_path, cam_folder))

    print(f"Dart camera {cam_index}, resolution: {resolution}, frame rate: {frame_rate}, cam_folder: {cam_folder_for_trial}")

    image_dump = []

    def capture_frame():
        
        ret, frame = cap.read()
        if not ret:
            print(f"Failed to acquire image from Dart camera.")
            return
        
        timestamp = time.time()
        image_dump.append((timestamp, frame))

    ready_path = 'C:/Users/Data acquisition/sensorimotorkit/assets/audio/Ready.wav'
    ready_wave = sa.WaveObject.from_wave_file(ready_path)
    ready_play = ready_wave.play()
    ready_play.wait_done()
    capture_frame()
    time.sleep(0.5)

    throw_path = 'C:/Users/Data acquisition/sensorimotorkit/assets/audio/Throw.wav'
    throw_wave = sa.WaveObject.from_wave_file(throw_path)
    throw_play = throw_wave.play()
    throw_play.wait_done()
    time.sleep(1)

    capture_frame()
    capture_frame()
    capture_frame()

    collect_path = 'C:/Users/Data acquisition/sensorimotorkit/assets/audio/Collect.wav'
    collect_wave = sa.WaveObject.from_wave_file(collect_path)
    collect_play = collect_wave.play()
    collect_play.wait_done()

    print(f"Saving images from dart camera {cam_index+1} to {cam_folder_for_trial}")
    for idx, (timestamp, frame) in enumerate(image_dump):
        cv2.imwrite(f"{cam_folder_for_trial}/frame_{idx}_{timestamp:.6f}.png", frame)

    cap.release()
    print(f"Acquisition complete for dart camera {cam_index+1}")

