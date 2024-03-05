import csv
import os
import cv2
from common.constants import Paths
import mediapipe as mp
import numpy as np
import re

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

def sort_key_func(file_name):
    numbers = re.findall(r'\d+', file_name)
    return int(numbers[0]) if numbers else 0

def apply_histograms(trial_path, raw_path, processed_path, output_name, frame_rate=30):

    raw_dir = os.path.normpath(os.path.join(trial_path, raw_path))
    processed_dir = os.path.normpath(os.path.join(trial_path, processed_path))

    raw_files = sorted(os.listdir(raw_dir), key=sort_key_func)
    processed_files = sorted(os.listdir(processed_dir), key=sort_key_func)

    if not raw_files:
        print(f"No files found in {raw_dir}. Exiting function.")
        return
    
    first_image_path = os.path.join(raw_dir, raw_files[0])
    first_image = cv2.imread(first_image_path)
    if first_image is None:
        print(f"Failed to read the first image from {first_image_path}. Exiting function.")
        return
    height, width = first_image.shape[:2]
    
    output_dir = os.path.dirname(processed_dir) 
    out = cv2.VideoWriter(
        os.path.normpath(os.path.join(output_dir, output_name)), 
        cv2.VideoWriter_fourcc(*'mp4v'), 
        frame_rate, 
        (width * 2, height)
    )

    for raw_file, processed_file in zip(raw_files, processed_files):
        raw_img_path = os.path.join(raw_dir, raw_file)
        processed_img_path = os.path.join(processed_dir, processed_file)
        raw_img = cv2.imread(raw_img_path)
        processed_img = cv2.imread(processed_img_path)
        
        hist = cv2.calcHist([raw_img], [0], None, [256], [0, 256])
        hist_img = np.zeros((height, 256, 3), dtype=np.uint8)
        cv2.normalize(hist, hist, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX) # is this accurate?

        for x, y in enumerate(hist):
            cv2.line(hist_img, (x, height), (x, height - int(y)), (255,255,255), 1)

        img_resized = cv2.resize(processed_img, (width, height))
        hist_img_resized = cv2.resize(hist_img, (width, height))

        concat_frame = np.hstack((img_resized, hist_img_resized))
        
        out.write(concat_frame)
    
    out.release()

def create_video_from_images(trial_path, image_path, output_name, frame_rate=30):
    img_dir = os.path.normpath(os.path.join(trial_path, image_path))
    image_files = sorted([f for f in os.listdir(img_dir) if f.endswith('.png')], key=sort_key_func)

    if not image_files:
        print(f"No images PNG found in {img_dir}. Exiting function.")
        return

    first_image_path = os.path.join(img_dir, image_files[0])
    first_image = cv2.imread(first_image_path)
    if first_image is None:
        print(f"Failed to read the first PNG image from {first_image_path}. Exiting function.")
        return
    height, width = first_image.shape[:2]

    output_dir = os.path.dirname(img_dir) 
    out = cv2.VideoWriter(
        os.path.normpath(os.path.join(output_dir, output_name)), 
        cv2.VideoWriter_fourcc(*'mp4v'), 
        frame_rate, 
        (width, height)
    )

    for image_file in image_files:
        img_path = os.path.join(img_dir, image_file)
        img = cv2.imread(img_path)

        if img is not None:
            out.write(img)

    out.release()
    print(f"Video saved at {os.path.join(output_dir, output_name)}")


def apply_pose_tracking_on_image(image_path, tracked_image_path=None):
    with mp_pose.Pose(static_image_mode=True) as pose:
        image = cv2.imread(image_path)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)
        
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
        if tracked_image_path:
            cv2.imwrite(tracked_image_path, image)
        else:
            cv2.imshow('Tracked Pose', image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        
        return results.pose_landmarks if results.pose_landmarks else None

def save_landmarks_to_csv(landmarks, csv_path):
    with open(csv_path, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        header = ['landmark', 'x', 'y', 'z', 'visibility']
        csv_writer.writerow(header)
        
        for i, landmark in enumerate(landmarks.landmark):
            csv_writer.writerow([i, landmark.x, landmark.y, landmark.z, landmark.visibility])

def process_images(trial_path, raw_path, processed_path):
    raw_dir = os.path.normpath(os.path.join(trial_path, raw_path))
    processed_dir = os.path.normpath(os.path.join(trial_path, processed_path))

    for file_name in os.listdir(raw_dir):
        image_path = os.path.join(raw_dir, file_name)
        processed_image_path = os.path.join(processed_dir, f"processed_{file_name}")
        # apply_pose_tracking_on_image(image_path, processed_image_path)
        landmarks = apply_pose_tracking_on_image(image_path, processed_image_path)
        
        if landmarks:
            csv_path = os.path.join(processed_dir, f"landmarks_{file_name}.csv")
            save_landmarks_to_csv(landmarks, csv_path)

def process_body_cam_images(trial_path):
    print("Applying pose tracking on body cam images")
    process_images(trial_path, Paths.BODY_LEFT_RAW_PATH, Paths.BODY_LEFT_PROCESSED_PATH)
    process_images(trial_path, Paths.BODY_RIGHT_RAW_PATH, Paths.BODY_RIGHT_PROCESSED_PATH)
    
    # print("Applying histograms on body cam images")
    # apply_histograms(trial_path, Paths.BODY_LEFT_PROCESSED_PATH, Paths.BODY_LEFT_PROCESSED_PATH,
    #                  "body_left_processed_with_hist.mp4")
    # apply_histograms(trial_path, Paths.BODY_RIGHT_PROCESSED_PATH, Paths.BODY_RIGHT_PROCESSED_PATH, 
    #                  "body_right_processed_with_hist.mp4")

    print("Creating video from body cam images")
    create_video_from_images(trial_path, Paths.BODY_LEFT_PROCESSED_PATH, "body_left_processed.mp4")
    create_video_from_images(trial_path, Paths.BODY_RIGHT_PROCESSED_PATH, "body_right_processed.mp4")
    create_video_from_images(trial_path, Paths.DARTBOARD_RAW_PATH, "dartboard_processed.mp4")
