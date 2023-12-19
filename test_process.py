from time import sleep

sleep_time = 1

def start_bodycam_left(trial_path): #TODO better state management for left and right
    print(f"[BODYCAM_LEFT] start")
    sleep(sleep_time)
    print(f"[BODYCAM_LEFT] end")

def start_bodycam_right(trial_path):
    print(f"[BODYCAM_RIGHT] start")
    sleep(sleep_time)
    print(f"[BODYCAM_RIGHT] end")

def start_dartcam(trial_path):
    print(f"[DARTCAM] start")
    sleep(sleep_time)
    print(f"[DARTCAM] end")

def start_gloves(trial_path):
    print("[GLOVES] start")
    sleep(sleep_time)
    print("[GLOVES] end")

def start_eeg(trial_path):
    print("[EEG] start")
    sleep(sleep_time)
    print("[EEG] end")

def capture_board(trial_path):
    print("[BOARD] start")
    sleep(sleep_time)
    print("[BOARD] end")

def run_feature_extraction(trial_path):
    print("[FE] start")
    sleep(sleep_time)
    print("[FE] end")