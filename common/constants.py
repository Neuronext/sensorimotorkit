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
    ACQUIRE_TIME = 1 # in seconds
    FRAME_RATE_BODY_CAM = 120 # Hz
    FRAME_RATE_DART_CAM = 30 # Hz
    RESOLUTION_BODY_CAM = (600, 960) # (height, width) in pixels
    RESOLUTION_DART_CAM = (480, 640) # (width, height) in pixels #TODO is this right?
    
    # EEG
    EEG_BOARD_ID = 2 
    EEG_SERIAL_PORT = 'COM3'
    EEG_FILE_NAME = Paths.EEG_PATH + '/eeg.csv'
    
    # EMG
    EMG_BOARD_ID = 1
    EMG_SERIAL_PORT = 'COM4'
    EMG_FILE_NAME = 'emg.csv'
    EMG_FILE_NAME = Paths.EMG_PATH + '/emg.csv'

    # Gloves
    GLOVE_IP = "127.0.0.1" #TODO is this the right IP? and are ports correct?
    GLOVE_PORT_RIGHT = 53450
    GLOVE_PORT_LEFT = 53451
    GLOVE_FILE_NAME = Paths.GLOVES_PATH + '/gloves.csv'
    GLOVE_HAND = "right" # is this right or is this wrong or is this left? lol


class MetadataConstants:

    TRIALS_PER_BATCH = 2
    BATCHES_PER_EXPERIMENT = 10
    TRAFFIC_LIGHT_SIZE = 20