import os
import time
import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.exit_codes import BrainFlowExitCodes

from common.constants import Paths, Constants
from common.common_utils import TrialManager
from common.board_utils import initialize_board

def stream_emg_data(duration):
    board = initialize_board(Constants.EEG_SERIAL_PORT, Constants.EEG_BOARD_ID)

    if board is None:
        print("[EMG] No data collected for this trial.")
        return 

    try:
        board.start_stream()
        time.sleep(duration)
        data = board.get_board_data()
        return data
    finally:
        board.stop_stream()
        board.release_session()

def collect_emg_data(duration, trial_path):
    emg_data = stream_emg_data(duration)
    if emg_data is None:
        print("[EMG] No data collected for this trial.")
        return
    
    emg_path = os.path.join(trial_path, Constants.EMG_FILE_NAME)
    TrialManager.save_data_to_csv(emg_data, emg_path)
    print(f"EMG data saved at {emg_data}")
