"""This module contain unit tests for the board class functionality"""

import traceback

from tests.tests import Tests
from models.board import Board
from models.consts import PrintColor, PlayerColor, PieceType, TestType, BOARD_START, ROWS, COLUMNS
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
                (Board.start_board([# Ideal case
                ['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR'],
                ['bP', 'bP', 'bP', '##', 'bP', 'bP', 'bP', 'bP'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', 'bP', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR'] 
                ], PlayerColor.black),
                 [(1,0,2,0)], True
                 ),
                (Board.start_board([# Case where pawn moves to a side without eating
                ['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR'],
                ['bP', 'bP', 'bP', '##', 'bP', 'bP', 'bP', 'bP'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', 'bP', '##', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR'] 
                ], PlayerColor.black),
                 [(1,0,2,1)], False
                 ),
                (Board.start_board([# Case where pawn moves to a side eating
                ['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR'],
                ['bP', 'bP', 'bP', '##', 'bP', 'bP', 'bP', 'bP'],
                ['##', 'wQ', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', 'bP', '##', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR'] 
                ], PlayerColor.black),
                 [(1,0,2,1)], True
                 ),
                (Board.start_board([# Case where pawn moves to a side eating when check locked
                ['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR'],
                ['bP', 'bP', 'bP', '##', 'bP', 'bP', 'bP', 'bP'],
                ['##', 'wQ', '##', '##', '##', 'wQ', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', 'bP', 'wR', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR'] 
                ], PlayerColor.black),
                 [(1,4,2,5)], False
                 ),
                (Board.start_board([# Case where pawn moves to the opposite direction
                ['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR'],
                ['bP', 'bP', 'bP', '##', 'bP', 'bP', 'bP', 'bP'],
                ['##', 'wQ', '##', '##', '##', 'wQ', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', 'bP', 'wR', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR'] 
                ], PlayerColor.black),
                 [(5,3,4,3)], False
                 )
            ]
            
            for i, case in enumerate(cases):
                performed = True
                for movement in case[1]:
                    if not case[0].move_piece(movement[0],movement[1],movement[2],movement[3]):
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
