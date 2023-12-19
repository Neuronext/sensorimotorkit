# import common packages
import multiprocessing
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from common import common_utils
from process import start_bodycam_left, start_bodycam_right, start_dartcam, start_gloves, start_eeg, capture_board


def run_trial(trial_path):

    processes = [
            multiprocessing.Process(target=start_bodycam_left, args=(trial_path,)),
            multiprocessing.Process(target=start_bodycam_right, args=(trial_path,)),
            multiprocessing.Process(target=start_dartcam, args=(trial_path,)),
            multiprocessing.Process(target=start_gloves, args=(trial_path,)),
            multiprocessing.Process(target=start_eeg, args=(trial_path,))
        ]
    
    for process in processes:
        process.start()

    for process in processes:
        process.join()

    #TODO capture_board()


if __name__ == '__main__':
    
    trial_path = common_utils.TrialManager.setup_trial(gui=False, data_path=None)
    print(f'Initialized the Trial Path: {os.path.normpath(trial_path)}')

    run_trial(trial_path) #TODO avoid passing trial_path everywhere
    print("Data collection complete, starting feature extraction...")
    # run feature extraction
    # run_feature_extraction(trial_path)
    print("feature extraction complete.")

