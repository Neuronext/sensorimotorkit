# constant.py
class Paths:
    EEG_PATH = "eeg"
    EMG_PATH = "emg"
    EYES_PATH = "eyes"
    GLOVES_PATH = "gloves"
    BODY_LEFT_RAW_PATH = "body_left/raw"
    BODY_RIGHT_RAW_PATH = "body_right/raw"
    DARTBOARD_RAW_PATH = "dart/raw"
    BODY_LEFT_PROCESSED_PATH = "body_left/processed"
    BODY_RIGHT_PROCESSED_PATH = "body_right/processed"
    
    @classmethod
    def __iter__(cls): #TODO items() should not be used, instead use __iter__
        for name in cls.__dict__:
            if not name.startswith('__') and not callable(getattr(cls, name)):
                yield name, getattr(cls, name) 

    @classmethod
    def items(cls):
        return ((name, getattr(cls, name)) for name in cls.__dict__ if not name.startswith("__") and not callable(getattr(cls, name)))


# Other constants
class Constants:
    # Camera
    ACQUIRE_TIME = 10
    FRAME_RATE_BODY_CAM = 120  
    FRAME_RATE_DART_CAM = 30
    RESOLUTION_BODY_CAM = (600, 960)
    RESOLUTION_DART_CAM = (480, 640)
    
    # EEG
    EEG_BOARD_ID = 2 
    EEG_SERIAL_PORT = 'COM3'
    EEG_FILE_NAME = 'eeg.csv'
    
    # EMG
    EMG_BOARD_ID = 1
    EMG_SERIAL_PORT = 'COM4'
    EMG_FILE_NAME = 'emg.csv'


#TODO is there a better way to do this?

