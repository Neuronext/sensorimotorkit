import datetime
import multiprocessing
import cv2
import os
from acquire_data.images.common_utils import init_structure
from acquire_data.images.body_cam import acquire_images_common
from acquire_data.images.dart_cam import acquire_dart_images

if __name__ == "__main__":
    date_folder = os.path.join("../", datetime.datetime.now().strftime("%Y-%m-%d"))
    print('------------------- main from images is being called -------------------')
    init_structure(date_folder)

    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    frame_rate_1 = 120.0  # Body cameras
    acquire_time = 1.0  # Acquire for 1 seconds

    barrier = multiprocessing.Barrier(3)

    process1 = multiprocessing.Process(target=acquire_images_common, args=(0, date_folder, None, frame_rate_1, barrier, 'body_tracking/camera_1', 10))
    process2 = multiprocessing.Process(target=acquire_images_common, args=(1, date_folder, None, frame_rate_1, barrier, 'body_tracking/camera_2', acquire_time))
    process3 = multiprocessing.Process(target=acquire_dart_images, args=(0, date_folder, None, 30, barrier, 'dart_tracking', acquire_time))

    process1.start()
    process2.start()
    process3.start()

    process1.join()
    process2.join()
    process3.join()

    cv2.destroyAllWindows()
