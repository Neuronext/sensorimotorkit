from time import sleep

def start_bodycam_left(trial_path): #TODO better state management for left and right
    print(f"[BODYCAM_LEFT] start")
    sleep(5)
    print(f"[BODYCAM_LEFT] end")

def start_bodycam_right(trial_path):
    print(f"[BODYCAM_RIGHT] start")
    sleep(5)
    print(f"[BODYCAM_RIGHT] end")

def start_dartcam(trial_path):
    print(f"[DARTCAM] start")
    sleep(5)
    print(f"[DARTCAM] end")

def start_gloves(trial_path):
    print("[GLOVES] start")
    sleep(5)
    print("[GLOVES] end")

def start_eeg(trial_path):
    print("[EEG] start")
    sleep(5)
    print("[EEG] end")

def capture_board(trial_path):
    print("[BOARD] start")
    sleep(5)
    print("[BOARD] end")

def run_feature_extraction(trial_path):
    print("[FE] start")
    sleep(5)
    print("[FE] end")