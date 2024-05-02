import os
from feature_extraction.apply_tracking import main

def process_trial(date, trial_num, draw_skeleton=False):
    trial_path = os.path.normpath(f"data/{date}/{trial_num}")
    print("Processing Body Cam Images for Trial: ", trial_path)
    main(trial_path, draw_skeleton=draw_skeleton)

if __name__ == "__main__":
    date = "2024-02-28"
    trial_num = "6"
    draw_skeleton = False
    process_trial(date, trial_num, draw_skeleton=draw_skeleton)
