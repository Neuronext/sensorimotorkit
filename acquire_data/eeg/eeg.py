import os
import time
import brainflow
import csv
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.exit_codes import BrainFlowExitCodes

from common.constants import Paths, Constants
from common.common_utils import TrialManager
from common.board_utils import initialize_board

def stream_eeg_data(duration):
    board = initialize_board(Constants.EEG_SERIAL_PORT, Constants.EEG_BOARD_ID)
    if board is None:
        print("[EEG] No data collected for this trail")
        return 

    try:
        board.start_stream()
        time.sleep(duration)
        data = board.get_board_data()
        return data
    finally:
        board.stop_stream()
        board.release_session()

def collect_eeg_data(duration, trial_path):
    eeg_data = stream_eeg_data(duration)
    if eeg_data is None:
        print("[EEG] No data collected for this trail")
        return

    eeg_path = os.path.join(trial_path, Constants.EEG_FILE_NAME)
    TrialManager.save_data_to_csv(eeg_data, eeg_path)