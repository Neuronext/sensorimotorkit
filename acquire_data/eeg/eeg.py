import os
import time
import brainflow
import csv
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.exit_codes import BrainFlowExitCodes
import logging
from common.constants import Paths, Constants
from common.common_utils import TrialManager
from common.board_utils import initialize_board
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal #TODO: PyQT5 imports should not be here, need to refactor
from common.board_manager import BoardManager


BoardShim.set_log_level(logging.ERROR) 

class EEGWorkerThread(QThread):
    data_collected = pyqtSignal(np.ndarray)

    def __init__(self, duration, board):
        super().__init__()
        self.duration = duration
        self.board = board

    def run(self):
        if self.board is None:
            print("[EEG] No board connected")
            return

        try:
            self.board.start_stream()
            start_time = time.time()
            while time.time() - start_time < self.duration:
                eeg_data = self.board.get_current_board_data(256) 
                if not eeg_data.size == 0:
                    self.data_collected.emit(eeg_data)
                time.sleep(0.1)  
        finally:
            self.board.stop_stream()
            self.board.release_session()


def plot_eeg_data(sampling_rate, eeg_data, channels):
    """Plot EEG data for given channels."""
    plt.figure()
    n_points = eeg_data.shape[1]
    times = np.linspace(0, n_points / sampling_rate, num=n_points)
    for channel in channels:
        plt.plot(times, eeg_data[channel, :], label=f'Channel {channel}')
    plt.xlabel('Time (s)')
    plt.ylabel('Voltage (microV)')
    plt.title('EEG Data')
    plt.legend()
    plt.show()


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

def load_and_plot_eeg_data(eeg_file_path):
    eeg_data = np.loadtxt(eeg_file_path, delimiter=',')
    sampling_rate = BoardShim.get_sampling_rate(Constants.EEG_BOARD_ID)
    eeg_data = eeg_data.T if eeg_data.shape[0] < eeg_data.shape[1] else eeg_data
    channels = np.arange(0, 32)  # Update this as needed
    plot_eeg_data(sampling_rate, eeg_data, channels)


def collect_eeg_data(duration, trial_path):
    board = BoardManager.get_board()
    if board is None:
        print("[EEG] No data collected for this trail")
        return
    
    eeg_data = stream_eeg_data(duration)
    if eeg_data is None:
        print("[EEG] No data collected for this trail")
        return

    eeg_path = os.path.join(trial_path, Constants.EEG_FILE_NAME)

    TrialManager.save_data_to_csv(eeg_data, eeg_path)    
    load_and_plot_eeg_data(eeg_path)

    print(f"EEG data saved at {eeg_path}")