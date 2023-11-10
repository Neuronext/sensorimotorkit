
import os
import pickle
from common_utils import convert_pickle_to_png, process_pkl_and_apply_pose
import datetime

date_folder = os.path.join("../../../", datetime.datetime.now().strftime("%Y-%m-%d"))

resolution_body_cam = (2, 600, 960)
resolution_dart_cam = (3, 480, 640)
curr = 10
process_pkl_and_apply_pose("../../2023-11-07/body_tracking/camera_1/raw/0", (800, 1200)) # (800, 1200)
process_pkl_and_apply_pose("../../2023-11-07/body_tracking/camera_2/raw/0", (800, 1200)) # (800, 1200)

# process_pkl_and_apply_pose("C:/Users/Data\ acquisition/sensorimotorkit/acquire_images/2023-11-06/body_tracking/2/", (800, 1200)) # (800, 1200)

# convert_pickle_to_png(os.path.join(date_folder, 'body_tracking/camera_2/raw', str(curr)), (600, 960)) # (600, 960)
# convert_pickle_to_png(os.path.join(date_folder, 'dart_tracking/raw', str(curr)), (480, 640, 3)) # (600, 960)
# C:\Users\Data acquisition\2023-11-07
