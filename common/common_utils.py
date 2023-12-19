# common_utils.py
import os
from datetime import datetime
from common.constants import Paths
import csv

class TrialManager:
    @staticmethod
    def get_base_path():
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'data')

    @staticmethod
    def get_today_str():
        return datetime.now().strftime('%Y-%m-%d')

    @staticmethod
    def get_trial_base_path(gui=False, data_path=None):
        if gui:
            base_path = data_path
        else:
            base_path = TrialManager.get_base_path()
        today_str = TrialManager.get_today_str()
        return os.path.join(base_path, today_str)

    @staticmethod
    def create_trial_path(trial_base_path):
        if not os.path.exists(trial_base_path):
            os.makedirs(trial_base_path)
        trial_number = len(os.listdir(trial_base_path))
        return os.path.join(trial_base_path, str(trial_number))
    
    @staticmethod
    def init_structure(trial_path):
        for name, relative_path in Paths.items():
            raw_path = os.path.normpath(os.path.join(trial_path, relative_path))
            full_path = os.path.abspath(raw_path)
            os.makedirs(full_path, exist_ok=True)
            # print(f"{name} path {full_path} created")

    @staticmethod
    def setup_trial(gui=False, data_path=None):
        # sloppy code incoming...., sorry
        trial_base_path = TrialManager.get_trial_base_path(gui=gui, data_path=data_path)
        trial_path = TrialManager.create_trial_path(trial_base_path)
        TrialManager.init_structure(trial_path)
        return trial_path
    
    @staticmethod
    def save_data_to_csv(data, file_path):
        print(f'Saving data to {file_path}')
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in data:
                writer.writerow(row)
