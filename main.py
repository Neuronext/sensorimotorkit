# import common packages
import multiprocessing
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


# import custom modules
from acquire_data.gloves import gloves
from acquire_data.eeg import eeg
from acquire_data.emg import emg
from acquire_data.images import body_cam, dart_cam
from common import common_utils
from common.constants import Paths
from common.constants import Constants 
from post_processing.apply_tracking import process_body_cam_images

def start_bodycam_left(trial_path): #TODO better state management for left and right
    print(f"Collecting bodycam left - cam_index 0 data")
    body_cam.acquire_images_common(0, trial_path, None, Constants.FRAME_RATE_BODY_CAM, None, Paths.BODY_LEFT_RAW_PATH, Constants.ACQUIRE_TIME)

def start_bodycam_right(trial_path):
    print(f"Collecting bodycam right - cam_index 1 data")
    body_cam.acquire_images_common(1, trial_path, None, Constants.FRAME_RATE_BODY_CAM, None, Paths.BODY_RIGHT_RAW_PATH, Constants.ACQUIRE_TIME)

#TODO untested
def start_dartcam(trial_path):
    print(f"Collecting bodycam right - cam_index 1 data")
    dart_cam.acquire_dart_images(0, trial_path, None, Constants.FRAME_RATE_DART_CAM, None, Paths.DARTBOARD_RAW_PATH, Constants.ACQUIRE_TIME)

def start_gloves(trial_path):
    print("Collecting gloves data")
    gloves.collect_glove_data(Constants.ACQUIRE_TIME, trial_path)

def start_eeg(trial_path):
    print("Collecting eeg data")
    eeg.collect_eeg_data(Constants.ACQUIRE_TIME, trial_path)

def capture_board(trial_path):
    print("capturing board") #TODO take a picture of the dart board

def run_trial(trial_path):

    #TODO can add a taskflow?
    proc_bodycam_left = multiprocessing.Process(target=start_bodycam_left, args=(trial_path,)) #TODO name it as right and left
    proc_bodycam_right = multiprocessing.Process(target=start_bodycam_right, args=(trial_path,))
    proc_gloves = multiprocessing.Process(target=start_gloves, args=(trial_path,))
    proc_eeg = multiprocessing.Process(target=start_eeg, args=(trial_path,))
    
    proc_bodycam_right.start()
    proc_bodycam_left.start()
    proc_gloves.start()
    proc_eeg.start()

    proc_bodycam_right.join()
    proc_bodycam_left.join()
    proc_gloves.join()
    proc_eeg.join()

    #TODO capture_board()


def run_post_processing(trial_path):
    print("Running post processing")
    process_body_cam_images(trial_path)

    #TODO run post processing

if __name__ == '__main__':
    
    trial_path = common_utils.TrialManager.setup_trial()
    print(f'Initialized the Trial Path: {os.path.normpath(trial_path)}')

    run_trial(trial_path) #TODO avoid passing trial_path everywhere, currently passed because folders get created multiple times
    print("Data collection complete, starting post processing...")
    # run post processing
    run_post_processing(trial_path) #TODO save these trail paths to a file so we can choose to run post processing all at once after all trials are done, it takes about 5 mins to run
    print("Post processing complete.")



#TODO
'''
data should be pushed to gcloud/s3 - preprocessing should handle this
all print statements should have a [MAIN] prefix associated with it
'''