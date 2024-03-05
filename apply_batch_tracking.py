import os
from feature_extraction.apply_tracking import process_body_cam_images

def process_trial(date, trial_num):
    trial_path = os.path.normpath(f"data/{date}/{trial_num}")
    print("Processing Body Cam Images...")
    process_body_cam_images(trial_path)

if __name__ == "__main__":
    date = "2024-02-15"
    trial_num = "2"
    process_trial(date, trial_num)
