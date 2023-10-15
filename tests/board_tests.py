"""This module contain unit tests for the board class functionalities"""

import traceback

from tests.tests import Tests
from models.board import Board
from models.consts import PrintColor, PlayerColor, PieceType, TestType, BOARD_START, ROWS, COLUMNS
from utils.utils import color_print

class BoardTests():
    @staticmethod
    @Tests.register_test(TestType.board)
    def board_start() -> bool:
        """Test for validating the correct board start values

        Returns:
            bool: Succes of the test.
        """

        try:
            board = Board.start_board()
            
            for r in range(len(ROWS)):
                for c in range(len(COLUMNS)):
                    if str(board.square(r,c)) != BOARD_START[r][c]:
                        color_print(f"The start board generated is not acurrate in square ({r},{c})", PrintColor.red)
                        return False
                
            color_print("Board Start PASSED", PrintColor.green)
            return True
        except Exception as e:
            color_print("Exception in start board:", PrintColor.red)
            print(e)
            traceback.print_exc()
            return False

    @staticmethod
    @Tests.register_test(TestType.board)
    def serialization() -> bool:
        """Test for validating the correct board start values

        Returns:
            bool: Succes of the test.
        """
        
        try:
            canCastleLeft = False
            canCastleRigth = True
            possibleEnPassant = (0,1)
            turn = PlayerColor.black
            
            board = Board.start_board()
            board.canCastleLeft = canCastleLeft
            board.canCastleRigth = canCastleRigth
            board.possibleEnPassant = possibleEnPassant
            board.turn = turn
            board.swap_pieces(1,0,2,0)
            
            if not board.serialize("data"):
                color_print("Board serialization failed", PrintColor.red)
                return False
            
            deserializedBoard = Board.deserialize("data")
            if deserializedBoard.canCastleLeft != canCastleLeft or board.canCastleRigth != canCastleRigth or deserializedBoard.possibleEnPassant != possibleEnPassant or\
                deserializedBoard.turn != turn or deserializedBoard.square(2,0).type != PieceType.pawn:
                    color_print("Board deserialization failed", PrintColor.red)
                    return False
            
            color_print("Board Serialization PASSED", PrintColor.green)
            return True
        except Exception as e:
            color_print("Exception in board serialization/deserialization:", PrintColor.red)
            print(e)
            traceback.print_exc()
            return False

    @staticmethod
    @Tests.register_test(TestType.board)
    def attacked_squares() -> bool:
        """Test for validating the calculation of the attacked squares

        Returns:
            bool: Succes of the test.
        """

        try:
            board = Board.start_board()
            
            cases = []
            board.squares_under_attack(PlayerColor.black)
            cases.append((board.attackedSquares, [(2,0),(2,1),(2,2),(2,3),(2,4),(2,5),(2,6),(2,7)]))#1
            board.squares_under_attack(PlayerColor.white)
            cases.append((board.attackedSquares, [(5,0),(5,1),(5,2),(5,3),(5,4),(5,5),(5,6),(5,7)]))#2
            board = Board.start_board([
                ['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR'],
                ['##', 'bP', 'bP', '##', 'bP', 'bP', 'bP', 'bP'],
                ['bP', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', 'bP', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR'] 
            ])
            board.squares_under_attack(PlayerColor.black)
            cases.append((board.attackedSquares, [(1,0),(2,1),(3,1),(2,2),(4,2),(1,3),(2,3),(2,4),(4,4),(2,5),(3,5),(2,6),(4,6),(2,7),(5,7)]))#3
            board = Board.start_board([
                ['bR', '##', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR'],
                ['##', 'bP', 'bP', '##', 'bP', 'bP', 'bP', 'bP'],
                ['bP', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', 'bP', '##', '##', '##', '##'],
                ['##', 'bK', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR'] 
            ])
            board.squares_under_attack(PlayerColor.black)
            cases.append((board.attackedSquares, [(1,0),(0,1),(2,1),(3,1),(2,2),(4,2),(1,3),(2,3),(2,4),(4,4),(2,5),(3,5),(2,6),(4,6),(2,7),(5,7),(5,3),(6,2),(6,0)]))#4
            
            for i, case in enumerate(cases):
                if len(case[0]) != len(case[1]):
                    color_print(F"Number of attacked squares wrong, Case #{i+1}", PrintColor.red)
                    print(f"Ideal: {case[1]}\nActual: {case[0]}")
                    return False
            
                for square in case[1]:
                    if square not in case[0]:
                        color_print(F"Missmatch in attacked squares: {square}, Case #{i}", PrintColor.red)
                        return False
                
            color_print("Board attacked squares calculation PASSED", PrintColor.green)
            return True
        except Exception as e:
            color_print("Exception in board attacked squares calculation:", PrintColor.red)
            print(e)
            traceback.print_exc()
            return False

    @staticmethod
    @Tests.register_test(TestType.board)    
    def checking() -> bool:
        """Test for validating the checking algorithm

        Returns:
            bool: Succes of the test.
        """

        try:
            # Format: (Board, Movements, Should be True?)
            cases = [
                (Board.start_board([
                ['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR'],
                ['bP', 'bP', 'bP', '##', 'bP', 'bP', 'bP', 'bP'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', 'bP', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR'] 
                ]),
                 [], False
                 ),
                (Board.start_board([
                ['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR'],
                ['bP', 'bP', 'bP', '##', 'bP', 'bP', 'bP', 'bP'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['wB', '##', '##', 'bP', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR'] 
                ]),
                 [], True
                 ),
                (Board.start_board([
                ['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR'],
                ['bP', 'bP', 'bP', '##', 'bP', 'bP', 'bP', 'bP'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', 'bP', '##', '##', '##', '##'],
                ['##', '##', '##', '##', 'wR', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR'] 
                ]),
                 [(5,4,1,4)], True
                 ),
                (Board.start_board([
                ['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR'],
                ['bP', 'bP', 'bP', '##', '##', 'bP', 'bP', 'bP'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', 'bP', 'wB', '##', '##', '##'],
                ['##', '##', '##', '##', 'wQ', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR'] 
                ]),
                 [(4,4,3,5)], False
                 )
            ]
            
            for i, case in enumerate(cases):
                for movement in case[1]:
                    if not case[0].move_piece(movement[0],movement[1],movement[2],movement[3]):
                        color_print(f"Movement not performed {movement}, in Case #{i}", PrintColor.yellow)
                        break
                    
                if case[0].check != case[2]:
                    color_print(F"Failed Case #{i+1} for Checking", PrintColor.red)
                    return False
                
            color_print("Checking PASSED", PrintColor.green)
            return True
        except Exception as e:
            color_print("Exception in Checking:", PrintColor.red)
            print(e)
            traceback.print_exc()
            return False

#TODO UnitTest for CheckMate

#TODO UnitTest for pawn