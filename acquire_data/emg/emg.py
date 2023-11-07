import time
import threading
import brainflow
import csv
from brainflow.board_shim import BoardShim, BrainFlowInputParams

def collect_eeg_data(serial_port, duration_in_seconds):
    params = BrainFlowInputParams()
    params.serial_port = serial_port
    
    board_id = 2  # OpenBCI Cyton over Bluetooth
    
    board = BoardShim(board_id, params)
    board.prepare_session()
    board.start_stream()

    time.sleep(duration_in_seconds)

    data = board.get_board_data()

    board.stop_stream()
    board.release_session()

    return data

def thread_function(serial_port, duration, save_path, file_name):
    eeg_data = collect_eeg_data(serial_port, duration)
    complete_save_path = save_path + "/" + file_name + ".csv"
    print(complete_save_path)
    with open(complete_save_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in eeg_data:
            writer.writerow(row)
    print("saved " + file_name)


def collect(duration, save_path):
    if __name__ == "__main__":
    
        # Assume your two EEG devices are on 'COM3' and 'COM4'
        t1 = threading.Thread(target=thread_function, args=('COM3',duration,save_path,"eeg"))
        # t2 = threading.Thread(target=thread_function, args=('COM4',duration,save_path,"emg"))

        t1.start()
        # t2.start()

        t1.join()
        # t2.join()