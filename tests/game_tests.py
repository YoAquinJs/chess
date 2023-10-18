"""This module contain unit tests for the board class functionality"""

import traceback

from tests.tests import Tests
from chess_engine.board import Board
from core.consts import PrintColor, PlayerColor, PieceType, TestType, BOARD_START, ROWS, COLUMNS
from utils.utils import color_print

#TODO everything
class GameTests():
    @staticmethod
    @Tests.register_test(TestType.game)
    def gameTests() -> bool:
        """Test for validating the moving algorithm for the pawn

        Returns:
            bool: Succes of the test.
        """

        try:
            # Format: (Board, Movements, Should be True?)
            cases = [
            ]
            
            for i, case in enumerate(cases):
                performed = True
                for movement in case[1]:
                    if not case[0].attempt_move(movement[0],movement[1],movement[2],movement[3])[0]:
                        performed = False
                        break
                    
                if performed != case[2]:
                    color_print(F"Failed Case #{i} for Pawn Movement", PrintColor.red)
                    return False
                
            color_print("Pawn Movement PASSED", PrintColor.green)
            return True
        except Exception as e:
            color_print("Exception in Pawn Movement:", PrintColor.red)
            print(e)
            traceback.print_exc()
            return False
