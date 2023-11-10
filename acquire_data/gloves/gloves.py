import os
import time
import socket
from common.constants import Constants
from common.common_utils import TrialManager

def get_glove_config():
    ip = Constants.GLOVE_IP
    port = Constants.GLOVE_PORT_RIGHT if Constants.GLOVE_HAND == "right" else Constants.GLOVE_PORT_LEFT
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(0.1)
    return ip, port, sock

def stream_glove_data(duration):
    ip, port, sock = get_glove_config()
    output = []
    end_time = time.time() + duration

    while time.time() < end_time:
        try:
            message = '{"type":"ping"}'.encode()
            sock.sendto(message, (ip, port))

            data, _ = sock.recvfrom(10000)
            output.append(data.decode())
        except socket.timeout:
            print("[Glove] Connection timed out")
            pass

    return output

def collect_glove_data(duration, trial_path):
    glove_data = stream_glove_data(duration)
    if not glove_data:
        print("[Glove] No data collected for this trial")
        return

    glove_path = os.path.join(trial_path, Constants.GLOVE_FILE_NAME)
    TrialManager.save_data_to_csv(glove_data, glove_path)
    print(f"Glove data saved at {glove_path}")
