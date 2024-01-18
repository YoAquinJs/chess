"""This module contain unit tests for the board class functionality"""

# Import external library 
import traceback

# Import Internal modules
from tests.tests import Tests
from chess_engine.board import Board
from game_logic.consts import PrintColor, PlayerColor, TestType, BOARD_START, ROWS, COLUMNS
from utils.utils import color_print

class PieceTests():
    """Test class containing Unit tests for the piece movement functionalities"""

    @staticmethod
    @Tests.register_test(TestType.piece)
    def pawn() -> bool:
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

    @staticmethod
    @Tests.register_test(TestType.piece)
    def bishop() -> bool:
        """Test for validating the moving algorithm for the bishop

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
                 [(0,2,2,4)], True
                 ),
                (Board.start_board([# case where bishop jumps piece
                ['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR'],
                ['bP', 'bP', 'bP', 'wP', 'bP', 'bP', 'bP', 'bP'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', 'bP', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR'] 
                ], PlayerColor.black),
                 [(0,2,2,4)], False
                 ),
                (Board.start_board([# Case where bishop moves when check locked
                ['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR'],
                ['bP', 'bP', 'bP', '##', 'bB', 'bP', 'bP', 'bP'],
                ['##', 'wQ', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', 'bP', 'wR', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR'] 
                ], PlayerColor.black),
                 [(1,4,3,6)], False
                 ),
                (Board.start_board([# Case where bishop moves like rook
                ['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR'],
                ['bP', 'bP', '##', '##', 'bP', 'bP', 'bP', 'bP'],
                ['##', 'wQ', '##', '##', '##', 'wQ', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', 'bP', 'wR', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR'] 
                ], PlayerColor.black),
                 [(0,2,5,2)], False
                 )
            ]
            
            for i, case in enumerate(cases):
                performed = True
                for movement in case[1]:
                    if not case[0].attempt_move(movement[0],movement[1],movement[2],movement[3])[0]:
                        performed = False
                        break
                    
                if performed != case[2]:
                    color_print(F"Failed Case #{i} for Bishop Movement", PrintColor.red)
                    return False
                
            color_print("Bishop Movement PASSED", PrintColor.green)
            return True
        except Exception as e:
            color_print("Exception in Bishop Movement:", PrintColor.red)
            print(e)
            traceback.print_exc()
            return False

    @staticmethod
    @Tests.register_test(TestType.piece)
    def knigth() -> bool:
        """Test for validating the moving algorithm for the knigth

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
                 [(0,1,2,0)], True
                 ),
                (Board.start_board([# Case where knigth moves like rook
                ['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR'],
                ['bP', 'bP', 'bP', '##', 'bP', 'bP', 'bP', 'bP'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', 'bP', '##', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR'] 
                ], PlayerColor.black),
                 [(0,1,2,1)], False
                 ),
                (Board.start_board([# case where knigth is check locked
                ['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR'],
                ['bP', 'bP', 'bP', '##', 'bK', 'bP', 'bP', 'bP'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', 'bP', '##', '##', '##', '##'],
                ['##', '##', '##', '##', 'wR', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR'] 
                ], PlayerColor.black),
                 [(1,4,3,3)], False
                 )
            ]
            
            for i, case in enumerate(cases):
                performed = True
                for movement in case[1]:
                    if not case[0].attempt_move(movement[0],movement[1],movement[2],movement[3])[0]:
                        performed = False
                        break
                    
                if performed != case[2]:
                    color_print(F"Failed Case #{i} for Knigth Movement", PrintColor.red)
                    return False
                
            color_print("Knigth Movement PASSED", PrintColor.green)
            return True
        except Exception as e:
            color_print("Exception in Knigth Movement:", PrintColor.red)
            print(e)
            traceback.print_exc()
            return False

    @staticmethod
    @Tests.register_test(TestType.piece)
    def rook() -> bool:
        """Test for validating the moving algorithm for the rook

        Returns:
            bool: Succes of the test.
        """

        try:
            # Format: (Board, Movements, Should be True?)
            cases = [
                (Board.start_board([# Ideal case
                ['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR'],
                ['##', 'bP', 'bP', '##', 'bP', 'bP', 'bP', 'bP'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', 'bP', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR'] 
                ], PlayerColor.black),
                 [(0,0,6,0)], True
                 ),
                (Board.start_board([# Case where rook moves like bishop
                ['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR'],
                ['bP', '##', 'bP', '##', 'bP', 'bP', 'bP', 'bP'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', 'bP', '##', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR'] 
                ], PlayerColor.black),
                 [(0,0,1,1)], False
                 ),
                (Board.start_board([# case where rook is check locked
                ['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR'],
                ['bP', 'bP', 'bP', '##', 'bR', 'bP', 'bP', 'bP'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', 'bP', '##', '##', '##', '##'],
                ['##', '##', '##', '##', 'wR', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR'] 
                ], PlayerColor.black),
                 [(1,4,1,3)], False
                 ),
                 (Board.start_board([# case where rook jumps a pawn
                ['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR'],
                ['bP', 'bP', '##', 'bP', 'bR', 'bP', 'bP', 'bP'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', 'bP', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR'] 
                ], PlayerColor.black),
                 [(1,4,1,2)], False
                 )
            ]
            
            for i, case in enumerate(cases):
                performed = True
                for movement in case[1]:
                    if not case[0].attempt_move(movement[0],movement[1],movement[2],movement[3])[0]:
                        performed = False
                        break
                    
                if performed != case[2]:
                    color_print(F"Failed Case #{i} for Rook Movement", PrintColor.red)
                    return False
                
            color_print("Rook Movement PASSED", PrintColor.green)
            return True
        except Exception as e:
            color_print("Exception in Rook Movement:", PrintColor.red)
            print(e)
            traceback.print_exc()
            return False

    @staticmethod
    @Tests.register_test(TestType.piece)
    def queen() -> bool:
        """Test for validating the moving algorithm for the queen

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
                 [(0,3,3,3)], True
                 ),
                (Board.start_board([# Ideal case
                ['bR', 'bK', 'bB', '##', 'b@', 'bB', 'bK', 'bR'],
                ['bP', 'bP', 'bP', '##', 'bP', 'bP', 'bP', 'bP'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', 'bQ', '##', '##', '##'],
                ['##', '##', '##', 'bP', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR'] 
                ], PlayerColor.black),
                 [(3,4,6,7)], True
                 ),
                (Board.start_board([# Case where the queen is check locked
                ['bR', 'bK', 'bB', '##', 'b@', 'bB', 'bK', 'bR'],
                ['bP', 'bP', 'bP', '##', 'bQ', 'bP', 'bP', 'bP'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', 'bP', 'wR', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR'] 
                ], PlayerColor.black),
                 [(1,4,2,5)], False
                 ),
                (Board.start_board([# case where queen jumps another piece
                ['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR'],
                ['bP', 'bP', 'bP', '##', 'bP', 'bP', 'bP', 'bP'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', 'bP', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR'] 
                ], PlayerColor.black),
                 [(0,3,2,5)], False
                 ),
                (Board.start_board([# case where queen moves like knigth
                ['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR'],
                ['bP', 'bP', 'bP', '##', 'bP', 'bP', 'bP', 'bP'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', 'bP', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR'] 
                ], PlayerColor.black),
                 [(0,3,2,4)], False
                 )
            ]
            
            for i, case in enumerate(cases):
                performed = True
                for movement in case[1]:
                    if not case[0].attempt_move(movement[0],movement[1],movement[2],movement[3])[0]:
                        performed = False
                        break
                    
                if performed != case[2]:
                    color_print(F"Failed Case #{i} for Queen Movement", PrintColor.red)
                    return False
                
            color_print("Queen Movement PASSED", PrintColor.green)
            return True
        except Exception as e:
            color_print("Exception in Queen Movement:", PrintColor.red)
            print(e)
            traceback.print_exc()
            return False

    @staticmethod
    @Tests.register_test(TestType.piece)
    def king() -> bool:
        """Test for validating the moving algorithm for the king

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
                 [(0,4,1,3)], True
                 ),
                (Board.start_board([# Ideal case
                ['bR', 'bK', 'bB', 'bQ', '##', 'bB', 'bK', 'bR'],
                ['bP', 'bP', 'bP', '##', 'bP', 'bP', 'bP', 'bP'],
                ['##', '##', '##', 'b@', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', 'bP', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR'] 
                ], PlayerColor.black),
                 [(2,3,2,4)], True
                 ),
                (Board.start_board([# Case where the square is attacked
                ['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR'],
                ['bP', 'bP', 'bP', '##', 'bP', 'bP', 'bP', 'bP'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', 'wR', '##', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR'] 
                ], PlayerColor.black),
                 [(0,4,1,3)], False
                 ),
                (Board.start_board([# case where after eating the eated piece could hack if not managed properly
                ['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR'],
                ['bP', 'bP', 'bP', 'wR', 'bP', 'bP', 'bP', 'bP'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', 'bP', '##', '##', '##', '##'],
                ['##', '##', '##', 'wR', '##', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'bQ', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR'] 
                ]),
                 [(7,4,6,4)], True
                 ),
                (Board.start_board([# case where the square is attacked after eating it
                ['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR'],
                ['bP', 'bP', 'bP', 'wR', 'bP', 'bP', 'bP', 'bP'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', 'wR', '##', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR'] 
                ], PlayerColor.black),
                 [(0,4,1,3)], False
                 )
            ]
            
            for i, case in enumerate(cases):
                performed = True
                for movement in case[1]:
                    if not case[0].attempt_move(movement[0],movement[1],movement[2],movement[3])[0]:
                        performed = False
                        break
                    
                if performed != case[2]:
                    color_print(F"Failed Case #{i} for King Movement", PrintColor.red)
                    return False
                
            color_print("King Movement PASSED", PrintColor.green)
            return True
        except Exception as e:
            color_print("Exception in King Movement:", PrintColor.red)
            print(e)
            traceback.print_exc()
            return False

    @staticmethod
    @Tests.register_test(TestType.piece)
    def castling() -> bool:
        """Test for validating the algorithm for determining if castling is possible

        Returns:
            bool: Succes of the test.
        """

        try:
            # Format: (Board, Movements, Should be True?)
            cases = [
                (Board.start_board([# Ideal Case
                ['bR', '##', '##', '##', 'b@', 'bB', 'bK', 'bR'],
                ['##', '##', '##', '##', 'bP', 'bP', 'bP', 'bP'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR']
                ], PlayerColor.black),
                 [(0,4,0,2)], True
                 ),
                (Board.start_board([# Case where piece in middle of king and tower
                ['bR', '##', '##', 'bB', 'b@', 'bB', 'bK', 'bR'],
                ['##', '##', '##', '##', 'bP', 'bP', 'bP', 'bP'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR']
                ], PlayerColor.black),
                 [(0,4,0,2)], False
                 ),
                (Board.start_board([# Case where final square is not empty
                ['bR', '##', 'bB', '##', 'b@', 'bB', 'bK', 'bR'],
                ['##', '##', '##', '##', 'bP', 'bP', 'bP', 'bP'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR']
                ], PlayerColor.black),
                 [(0,4,0,2)], False
                 ),
                (Board.start_board([# Case where piece in middle of king and tower
                ['bR', 'bB', '##', '##', 'b@', 'bB', 'bK', 'bR'],
                ['##', '##', '##', '##', 'bP', 'bP', 'bP', 'bP'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR']
                ], PlayerColor.black),
                 [(0,4,0,2)], False
                 ),
                (Board.start_board([# case with attacked square in king's path
                ['bR', '##', '##', '##', 'b@', 'bB', 'bK', 'bR'],
                ['##', '##', '##', '##', 'bP', 'bP', 'bP', 'bP'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', 'wQ', '##', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', '##', 'w@', 'wB', 'wK', 'wR']
                ], PlayerColor.black),
                 [(0,4,0,2)], False
                 ),
                (Board.start_board([# case with attacked square where king castles
                ['bR', '##', '##', '##', 'b@', 'bB', 'bK', 'bR'],
                ['##', '##', '##', '##', 'bP', 'bP', 'bP', 'bP'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', 'wQ', '##', '##', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', '##', 'w@', 'wB', 'wK', 'wR']
                ], PlayerColor.black),
                 [(0,4,0,2)], False
                 ),
                (Board.start_board([# case with king checked
                ['bR', '##', '##', '##', 'b@', 'bB', 'bK', 'bR'],
                ['##', '##', '##', '##', 'bP', 'bP', 'bP', 'bP'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['wQ', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', '##', 'w@', 'wB', 'wK', 'wR']
                ], PlayerColor.black),
                 [(0,4,0,2)], False
                 ),
                (Board.start_board([# case where king moves
                ['bR', '##', '##', '##', 'b@', 'bB', 'bK', 'bR'],
                ['##', '##', '##', '##', 'bP', 'bP', 'bP', 'bP'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['wQ', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', '##', 'w@', 'wB', 'wK', 'wR']
                ], PlayerColor.black),
                 [(0,4,0,3),(0,3,0,4)], False
                 ),
                (Board.start_board([ # case where tower moves
                ['bR', '##', '##', '##', 'b@', 'bB', 'bK', 'bR'],
                ['##', '##', '##', '##', 'bP', 'bP', 'bP', 'bP'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['wQ', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', '##', 'w@', 'wB', 'wK', 'wR']
                ], PlayerColor.black),
                 [(0,0,0,1),(6,0,5,0),(0,1,0,0),(6,1,5,1),(0,4,0,2)], False
                 ),
            ]
            
            for i, case in enumerate(cases):
                performed = True
                for movement in case[1]:
                    if not case[0].attempt_move(movement[0],movement[1],movement[2],movement[3])[0]:
                        performed = False
                        break
                
                if performed != case[2]:
                    color_print(F"Failed Case #{i} for castling", PrintColor.red)
                    return False
                
            color_print("Castling PASSED", PrintColor.green)
            return True
        except Exception as e:
            color_print("Exception in Castling:", PrintColor.red)
            print(e)
            traceback.print_exc()
            return False

    @staticmethod
    @Tests.register_test(TestType.piece)
    def enpassant() -> bool:
        """Test for validating the enpassant algorithm

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
                ]),
                 [(6,2,4,2),(4,3,5,2)], True
                 ),
                (Board.start_board([# Case where pawn is not in the correct positon
                ['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR'],
                ['bP', 'bP', 'bP', '##', 'bP', 'bP', 'bP', 'bP'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', 'bP', '##', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR'] 
                ]),
                 [(6,2,4,2),(5,3,6,2)], False
                 ),
                (Board.start_board([# case where en passant is made without double pawn jump
                ['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR'],
                ['bP', 'bP', 'bP', '##', 'bP', 'bP', 'bP', 'bP'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', 'bP', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR'] 
                ], PlayerColor.black),
                 [(4,3,6,2)], False
                 )
            ]
            
            for i, case in enumerate(cases):
                performed = True
                for movement in case[1]:
                    if not case[0].attempt_move(movement[0],movement[1],movement[2],movement[3])[0]:
                        performed = False
                        break
                    
                if performed != case[2]:
                    color_print(F"Failed Case #{i} for Enpassant", PrintColor.red)
                    return False
                
            color_print("Enpassant PASSED", PrintColor.green)
            return True
        except Exception as e:
            color_print("Exception in Enpassant:", PrintColor.red)
            print(e)
            traceback.print_exc()
            return False

    @staticmethod
    @Tests.register_test(TestType.piece)
    def double_pawn_move() -> bool:
        """Test for validating the algorithm forthe double pawn move

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
                 [(1,0,3,0)], True
                 ),
                (Board.start_board([# Case where pawn had already moved
                ['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR'],
                ['##', 'bP', 'bP', '##', 'bP', 'bP', 'bP', 'bP'],
                ['bP', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', 'bP', '##', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR'] 
                ], PlayerColor.black),
                 [(2,0,4,0)], False
                 ),
                (Board.start_board([# case where pawn moves, and then tries to double move
                ['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR'],
                ['bP', 'bP', 'bP', '##', 'bP', 'bP', 'bP', 'bP'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', 'bP', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR'] 
                ], PlayerColor.black),
                 [(1,0,2,0),(6,0,5,0),(2,0,4,0)], False
                 )
            ]
            
            for i, case in enumerate(cases):
                performed = True
                for movement in case[1]:
                    if not case[0].attempt_move(movement[0],movement[1],movement[2],movement[3])[0]:
                        performed = False
                        break
                    
                if performed != case[2]:
                    color_print(F"Failed Case #{i} for Double pawn move", PrintColor.red)
                    return False
                
            color_print("Double pawn move PASSED", PrintColor.green)
            return True
        except Exception as e:
            color_print("Exception in Double pawn move:", PrintColor.red)
            print(e)
            traceback.print_exc()
            return False
