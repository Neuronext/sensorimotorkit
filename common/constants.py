# constant.py
class MetadataConstants:

    TRIALS_PER_BATCH = 1
    BATCHES_PER_EXPERIMENT = 1
    TRAFFIC_LIGHT_SIZE = 20
    METADATA_FILE_NAME = 'metadata.csv'
    POLLING_INTERVAL = 100 # ms
    SLEEP_TIME_BETWEEN_TRIALS = 3 # s

    METADATA_FILE_NAME = 'metadata.csv'

    ENABLE_BODY_CAM = True
    ENABLE_DART_CAM = True
    ENABLE_EEG = False
    ENABLE_EMG = False
    ENABLE_GLOVES = False
    ENABLE_EYES = False

    CAMERA = "spinview" # "spinview" or "opencv"

# PLEASE DO NOT CHANGE THE FOLLOWING
class Components:
    
    ENABLED_COMPONENTS = {
        'bodycam_left': MetadataConstants.ENABLE_BODY_CAM,
        'bodycam_right': MetadataConstants.ENABLE_BODY_CAM,
        'dartcam': MetadataConstants.ENABLE_DART_CAM,
        'eeg': MetadataConstants.ENABLE_EEG,
        'gloves': MetadataConstants.ENABLE_GLOVES
    }

class Paths:
    EEG_PATH = "eeg" if MetadataConstants.ENABLE_EEG else None
    EMG_PATH = "emg" if MetadataConstants.ENABLE_EMG else None
    EYES_PATH = "eyes" if MetadataConstants.ENABLE_EYES else None
    GLOVES_PATH = "gloves" if MetadataConstants.ENABLE_GLOVES else None
    BODY_LEFT_RAW_PATH = "body_left/raw" if MetadataConstants.ENABLE_BODY_CAM else None
    BODY_RIGHT_RAW_PATH = "body_right/raw" if MetadataConstants.ENABLE_BODY_CAM else None
    DARTBOARD_RAW_PATH = "dart/raw" if MetadataConstants.ENABLE_DART_CAM else None
    BODY_LEFT_PROCESSED_PATH = "body_left/processed" if MetadataConstants.ENABLE_BODY_CAM else None
    BODY_RIGHT_PROCESSED_PATH = "body_right/processed" if MetadataConstants.ENABLE_BODY_CAM else None
    
    @classmethod
    def __iter__(cls): #TODO items() should not be used, instead use __iter__
        for name, value in cls.__dict__.items():
            if not name.startswith('__') and not callable(value) and value is not None:
                yield name, value

    @classmethod
    def items(cls):
        return ((name, getattr(cls, name)) for name in cls.__dict__ if not name.startswith("__") and not callable(getattr(cls, name)))



# Other constants
class Constants:

    # GUI
    TRAFFIC_LIGHT_SIZE = 20 # pixels

    # Camera
    ACQUIRE_TIME = 10 # in seconds
    FRAME_RATE_BODY_CAM = 120 # Hz
    FRAME_RATE_DART_CAM = 30 # Hz
    RESOLUTION_BODY_CAM = (600, 960) # (height, width) in pixels
    RESOLUTION_DART_CAM = (480, 640) # (width, height) in pixels #TODO is this right?
    
    # EEG
    if MetadataConstants.ENABLE_EEG == True:
        EEG_BOARD_ID = 2 
        EEG_SERIAL_PORT = 'COM3'
        EEG_FILE_NAME = Paths.EEG_PATH + '/eeg.csv'
    
    # EMG
    if MetadataConstants.ENABLE_EMG == True:
        EMG_BOARD_ID = 1
        EMG_SERIAL_PORT = 'COM4'
        EMG_FILE_NAME = 'emg.csv'
        EMG_FILE_NAME = Paths.EMG_PATH + '/emg.csv' 

    # Gloves
    if MetadataConstants.ENABLE_GLOVES == True:
        GLOVE_IP = "127.0.0.1" #TODO is this the right IP? and are ports correct?
        GLOVE_PORT_RIGHT = 53450
        GLOVE_PORT_LEFT = 53451
        GLOVE_FILE_NAME = Paths.GLOVES_PATH + '/gloves.csv'
        GLOVE_HAND = "right" # is this right or is this wrong or is this left? lol


