# import common packages
import multiprocessing
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from common import common_utils
from common.constants import Components
from process import start_bodycam_left, start_bodycam_right, start_dartcam, start_gloves, start_eeg, capture_board, process_body_cam_images


def run_trial(trial_path):

    processes = {}
    for component, enabled in Components.ENABLED_COMPONENTS.items():
        if enabled:
            process_function = globals()[f"start_{component}"] 
            processes[component] = multiprocessing.Process(target=process_function, args=(trial_path,))
            
    for _, process in processes.items():
        process.start()

    for _, process in processes.items():
        process.join()


    #TODO capture_board()


def run_feature_extraction(trial_path):
    print("Running feature extraction")
    process_body_cam_images(trial_path)

if __name__ == '__main__':
    
    trial_path = common_utils.TrialManager.setup_trial(gui=False, data_path=None)
    print(f'Initialized the Trial Path: {os.path.normpath(trial_path)}')

    run_trial(trial_path)
    print("Data collection complete, starting feature extraction...")
    # run feature extraction
    # run_feature_extraction(trial_path)
    print("feature extraction complete.")

