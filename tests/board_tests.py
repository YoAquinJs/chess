"""This module contain unit tests for the board class functionality"""

from tests.tests import Tests
from models.board import Board
from models.consts import PrintColor, PlayerColor, PieceType, BOARD_START, ROWS, COLUMNS
from utils.utils import color_print

class BoardTests():
    @Tests.register_test
    @staticmethod
    def board_start() -> bool:
        """Test for validating the correct board start values

        Returns:
            bool: Succes of the test.
        """

        try:
            board = Board.start_board()
            
            for r in range(len(ROWS)):
                for c in range(len(COLUMNS)):
                    if str(board.select_square(r,c)) != BOARD_START[r][c]:
                        color_print(f"The start board generated is not acurrate in square ({r},{c})", PrintColor.red)
                        return False
                
            color_print("Board Start PASSED", PrintColor.green)
            return True
        except Exception as e:
            color_print(f"Exception in start board:", PrintColor.red)
            print(e)
            return False

    @Tests.register_test
    @staticmethod
    def serialization() -> bool:
        """Test for validating the correct board start values

        Returns:
            bool: Succes of the test.
        """
        
        try:
            board = Board.start_board()
            board.canCastle = False
            board.possibleEnPassant = (0,1)
            board.turn = PlayerColor.black
            board.swap_pieces(1,0,2,0)
            
            if not board.serialize("data"):
                color_print("Board serialization failed", PrintColor.red)
                return False
            
            deserializedBoard = Board.deserialize("data")
            if deserializedBoard.canCastle != False or deserializedBoard.possibleEnPassant != (0,1) or\
                deserializedBoard.turn != PlayerColor.black or deserializedBoard.select_square(2,0).type != PieceType.pawn:
                    color_print("Board deserialization failed", PrintColor.red)
                    return False
            
            color_print("Board Serialization PASSED", PrintColor.green)
            return True
        except Exception as e:
            color_print(f"Exception in board serialization/deserialization:", PrintColor.red)
            print(e)
            return False
