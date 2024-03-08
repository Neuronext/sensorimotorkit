from common.board_utils import initialize_board, handle_brainflow_error
from common.constants import Constants

class BoardManager:
    _board = None

    @classmethod
    def get_board(cls):
        if cls._board is None:
            try:
                cls._board = initialize_board(Constants.EEG_SERIAL_PORT, Constants.EEG_BOARD_ID)
            except Exception as e:
                handle_brainflow_error(e)
        return cls._board
