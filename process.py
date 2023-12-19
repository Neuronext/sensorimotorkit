

# import custom modules
from acquire_data.gloves import gloves
from acquire_data.eeg import eeg
from acquire_data.emg import emg
from acquire_data.images import body_cam, dart_cam
from common.constants import Paths
from common.constants import Constants 
from feature_extraction.apply_tracking import process_body_cam_images


def start_bodycam_left(trial_path): #TODO better state management for left and right
    print(f"Collecting bodycam left - cam_index 0 data")
    body_cam.acquire_images_common(0, trial_path, None, Constants.FRAME_RATE_BODY_CAM, None, Paths.BODY_LEFT_RAW_PATH, Constants.ACQUIRE_TIME)

def start_bodycam_right(trial_path):
    print(f"Collecting bodycam right - cam_index 1 data")
    body_cam.acquire_images_common(1, trial_path, None, Constants.FRAME_RATE_BODY_CAM, None, Paths.BODY_RIGHT_RAW_PATH, Constants.ACQUIRE_TIME)

def start_dartcam(trial_path):
    print(f"Collecting dartcam")
    dart_cam.acquire_dart_images(0, trial_path, None, Constants.FRAME_RATE_DART_CAM, None, Paths.DARTBOARD_RAW_PATH, Constants.ACQUIRE_TIME)

def start_gloves(trial_path):
    print("Collecting gloves data")
    gloves.collect_glove_data(Constants.ACQUIRE_TIME, trial_path)

def start_eeg(trial_path):
    print("Collecting eeg data")
    eeg.collect_eeg_data(Constants.ACQUIRE_TIME, trial_path)

def capture_board(trial_path):
    print("capturing board") #TODO take a picture of the dart board

def run_feature_extraction(trial_path):
    print("Running feature extraction")
    process_body_cam_images(trial_path)