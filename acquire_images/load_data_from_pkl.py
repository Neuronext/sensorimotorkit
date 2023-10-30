import pickle
import cv2
import numpy as np

resolution = (2048, 2448)
with open("path/to/saved/file.pkl", "rb") as f:
    raw_data = pickle.load(f)

frame = np.array(raw_data).reshape(resolution)
frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)


# (1200, 960)
# (600, 960)
