
import os
import cv2
from common.constants import Paths
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

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

def process_images(trial_path, raw_path, processed_path, process_function):
    raw_dir = os.path.normpath(os.path.join(trial_path, raw_path))
    processed_dir = os.path.normpath(os.path.join(trial_path, processed_path))

    for file_name in os.listdir(raw_dir):
        image_path = os.path.join(raw_dir, file_name)
        processed_image_path = os.path.join(processed_dir, f"processed_{file_name}")
        apply_pose_tracking_on_image(image_path, processed_image_path)

def process_body_cam_images(trial_path):
    process_images(trial_path, Paths.BODY_LEFT_RAW_PATH, Paths.BODY_LEFT_PROCESSED_PATH)
    process_images(trial_path, Paths.BODY_RIGHT_RAW_PATH, Paths.BODY_RIGHT_PROCESSED_PATH)

