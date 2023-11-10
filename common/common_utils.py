# common_utils.py
import os
from datetime import datetime
from common.constants import Paths

class TrialManager:
    @staticmethod
    def get_base_path():
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'data')

    @staticmethod
    def get_today_str():
        return datetime.now().strftime('%Y-%m-%d')

    @staticmethod
    def get_trial_base_path():
        base_path = TrialManager.get_base_path()
        today_str = TrialManager.get_today_str()
        return os.path.join(base_path, today_str)

    @staticmethod
    def create_trial_path(trial_base_path):
        if not os.path.exists(trial_base_path):
            os.makedirs(trial_base_path)
        trial_number = len(os.listdir(trial_base_path))
        return os.path.join(trial_base_path, str(trial_number)), trial_number
    
    @staticmethod
    def init_structure(trial_path):
        for name, relative_path in Paths.items():
            raw_path = os.path.normpath(os.path.join(trial_path, relative_path))
            full_path = os.path.abspath(raw_path)
            os.makedirs(full_path, exist_ok=True)
            # print(f"{name} path {full_path} created")

    @staticmethod
    def setup_trial():
        trial_base_path = TrialManager.get_trial_base_path()
        trial_path, trial_number = TrialManager.create_trial_path(trial_base_path)
        TrialManager.init_structure(trial_path)
        return trial_path, trial_number