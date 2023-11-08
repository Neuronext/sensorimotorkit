# import common packages
import multiprocessing
import os
from datetime import datetime

# import custom modules
from acquire_data.gloves import gloves
from acquire_data.eeg import eeg
from acquire_data.emg import emg
from acquire_data.images import body_cam, dart_cam, common_utils, main

base_path = r'./data/'
today_str = datetime.now().strftime('%Y-%m-%d')
curr_trial_path = os.path.join(base_path, today_str)
if not os.path.exists(curr_trial_path):
    os.makedirs(curr_trial_path)

common_utils.init_structure(curr_trial_path)
print(f"folder {curr_trial_path} structure initialized")
acquire_time = 10

def get_save_path():
    base_path = "../data/"
    today_str = datetime.now().strftime('%Y-%m-%d')
    folder_path = os.path.join(base_path, today_str)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    
    todays_trials = os.listdir(folder_path)
    trial_number = len(todays_trials)
    trial_path = os.path.join(folder_path, str(trial_number))
    os.makedirs(trial_path)
    return trial_path


def start_bodycam(save_path, cam_index):
    print("collecting bodycam data for camera " + str(cam_index+1))
    body_cam.acquire_images_common(cam_index, curr_trial_path, None, 120, None, f'body_tracking/camera_{cam_index+1}', acquire_time)

def start_gloves(save_path):
    print("collecting gloves data")
    gloves.collect(acquire_time, save_path)

def start_eeg(save_path):
    print("collecting eeg")
    eeg.collect(acquire_time, save_path)

def capture_board(save_path):
    print("capturing board")

def run_trial():
    save_path = get_save_path()

    proc_bodycam_0 = multiprocessing.Process(target=start_bodycam, args=(save_path,0)) #TODO name it as right and left
    proc_bodycam_1 = multiprocessing.Process(target=start_bodycam, args=(save_path,1))
    proc_gloves = multiprocessing.Process(target=start_gloves, args=(save_path,))
    proc_eeg = multiprocessing.Process(target=start_eeg, args=(save_path,))
    
    proc_bodycam_0.start()
    proc_bodycam_1.start()
    proc_gloves.start()
    proc_eeg.start()

    proc_bodycam_0.join()
    proc_bodycam_1.join()
    proc_gloves.join()
    proc_eeg.join()


    proc_bodycam_0.terminate()
    proc_bodycam_1.terminate()
    proc_gloves.terminate()
    proc_eeg.terminate()

    capture_board(save_path)

if __name__ == '__main__':
    run_trial()


#TODO
'''
remove save path from all functions
get some global values like frame rate etc
data should be pushed to gcloud or something - preprocessing should do this
'''