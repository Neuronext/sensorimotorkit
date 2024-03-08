# board_utils.py
import socket
from common.constants import Constants
import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.exit_codes import BrainFlowExitCodes
from common.constants import Constants
import inspect

def handle_brainflow_error(e):
    if e.exit_code == BrainFlowExitCodes.BOARD_NOT_CREATED_ERROR:
        print("Error: Board not created. Ensure the device is connected and try again.")
    elif e.exit_code == BrainFlowExitCodes.STATUS_OK_ERROR:
        print("Board is already initialized.")
    else:
        print(f"BrainFlowError encountered: {e}")

def initialize_board(serial_port, board_id):
    caller_name = inspect.stack()[1].function
    print(f"Called by {caller_name}")
    print(f"Initializing board with serial port {serial_port} and board ID {board_id}")
    try:
        params = BrainFlowInputParams()
        params.serial_port = serial_port
        board = BoardShim(board_id, params)
        board.prepare_session()
        return board
    except brainflow.exit_codes.BrainFlowError as e:
        handle_brainflow_error(e)
        return None