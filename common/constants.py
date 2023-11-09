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
ACQUIRE_TIME = 10
FRAME_RATE = 120  


#TODO is there a better way to do this?

