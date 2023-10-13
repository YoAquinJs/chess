"""This module contain unit tests for the board class functionality"""

from tests.tests import Tests
from models.board import Board
from models.consts import PrintColor, PlayerColor, PieceType, BOARD_START, ROWS, COLUMNS
from utils.utils import color_print

class BoardTests():
    @staticmethod
    @Tests.register_test
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
            color_print("Exception in start board:", PrintColor.red)
            print(e)
            return False

    @staticmethod
    @Tests.register_test
    def serialization() -> bool:
        """Test for validating the correct board start values

        Returns:
            bool: Succes of the test.
        """
        
        try:
            canCastle = False
            possibleEnPassant = (0,1)
            turn = PlayerColor.black
            
            board = Board.start_board()
            board.canCastle = canCastle
            board.possibleEnPassant = possibleEnPassant
            board.turn = turn
            board.swap_pieces(1,0,2,0)
            
            if not board.serialize("data"):
                color_print("Board serialization failed", PrintColor.red)
                return False
            
            deserializedBoard = Board.deserialize("data")
            if deserializedBoard.canCastle != canCastle or deserializedBoard.possibleEnPassant != possibleEnPassant or\
                deserializedBoard.turn != turn or deserializedBoard.select(2,0).type != PieceType.pawn:
                    color_print("Board deserialization failed", PrintColor.red)
                    return False
            
            color_print("Board Serialization PASSED", PrintColor.green)
            return True
        except Exception as e:
            color_print("Exception in board serialization/deserialization:", PrintColor.red)
            print(e)
            return False

    @staticmethod
    @Tests.register_test
    def attacked_squares() -> bool:
        """Test for validating the calculation of the attacked squares

        Returns:
            bool: Succes of the test.
        """

        try:
            board = Board.start_board()
            
            cases = []
            board.squares_under_attack(PlayerColor.black)
            cases.append((board.attackedSquares, [(2,0),(2,1),(2,2),(2,3),(2,4),(2,5),(2,6),(2,7)]))
            board.squares_under_attack(PlayerColor.white)
            cases.append((board.attackedSquares, [(5,0),(5,1),(5,2),(5,3),(5,4),(5,5),(5,6),(5,7)]))
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
            cases.append((board.attackedSquares, [(1,0),(2,1),(3,1),(2,2),(4,2),(1,3),(2,3),(2,4),(4,4),(2,5),(3,5),(2,6),(4,6),(2,7),(5,7)]))
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
            cases.append((board.attackedSquares, [(1,0),(2,1),(3,1),(2,2),(4,2),(1,3),(2,3),(2,4),(4,4),(2,5),(3,5),(2,6),(4,6),(2,7),(5,7),(5,3),(6,2),(6,0)]))
            
            for i, case in enumerate(cases):
                if len(case[0]) != len(case[1]):
                    color_print(F"Number of attacked squares wrong, Case #{i}", PrintColor.red)
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
            return False

    @staticmethod
    @Tests.register_test
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
                ]),
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
                ]),
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
                ]),
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
                ]),
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
                ]),
                 [(5,3,4,3)], False
                 )
            ]
            
            for i, case in enumerate(cases):
                performed = True
                for movement in case[1]:
                    if not case[0].move_piece(movement[0],movement[1],movement[2],movement[3]):
                        performed = False
                        break
                    
                if performed != case[3]:
                    color_print(F"Failed Case #{i} for Pawn Movement", PrintColor.red)
                    return False
                
            color_print("Pawn Movement PASSED", PrintColor.green)
            return True
        except Exception as e:
            color_print("Exception in Pawn Movement:", PrintColor.red)
            print(e)
            return False

    @staticmethod
    @Tests.register_test
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
                ]),
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
                ]),
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
                ]),
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
                ]),
                 [(0,2,5,2)], False
                 )
            ]
            
            for i, case in enumerate(cases):
                performed = True
                for movement in case[1]:
                    if not case[0].move_piece(movement[0],movement[1],movement[2],movement[3]):
                        performed = False
                        break
                    
                if performed != case[3]:
                    color_print(F"Failed Case #{i} for Bishop Movement", PrintColor.red)
                    return False
                
            color_print("Bishop Movement PASSED", PrintColor.green)
            return True
        except Exception as e:
            color_print("Exception in Bishop Movement:", PrintColor.red)
            print(e)
            return False

    @staticmethod
    @Tests.register_test
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
                ]),
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
                ]),
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
                ]),
                 [(1,4,3,3)], False
                 )
            ]
            
            for i, case in enumerate(cases):
                performed = True
                for movement in case[1]:
                    if not case[0].move_piece(movement[0],movement[1],movement[2],movement[3]):
                        performed = False
                        break
                    
                if performed != case[3]:
                    color_print(F"Failed Case #{i} for Knigth Movement", PrintColor.red)
                    return False
                
            color_print("Knigth Movement PASSED", PrintColor.green)
            return True
        except Exception as e:
            color_print("Exception in Knigth Movement:", PrintColor.red)
            print(e)
            return False

    @staticmethod
    @Tests.register_test
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
                ]),
                 [(0,0,0,6)], True
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
                ]),
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
                ]),
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
                ]),
                 [(1,4,1,2)], False
                 )
            ]
            
            for i, case in enumerate(cases):
                performed = True
                for movement in case[1]:
                    if not case[0].move_piece(movement[0],movement[1],movement[2],movement[3]):
                        performed = False
                        break
                    
                if performed != case[3]:
                    color_print(F"Failed Case #{i} for Rook Movement", PrintColor.red)
                    return False
                
            color_print("Rook Movement PASSED", PrintColor.green)
            return True
        except Exception as e:
            color_print("Exception in Rook Movement:", PrintColor.red)
            print(e)
            return False

    @staticmethod
    @Tests.register_test
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
                ]),
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
                ]),
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
                ]),
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
                ]),
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
                ]),
                 [(0,3,2,4)], False
                 )
            ]
            
            for i, case in enumerate(cases):
                performed = True
                for movement in case[1]:
                    if not case[0].move_piece(movement[0],movement[1],movement[2],movement[3]):
                        performed = False
                        break
                    
                if performed != case[3]:
                    color_print(F"Failed Case #{i} for Queen Movement", PrintColor.red)
                    return False
                
            color_print("Queen Movement PASSED", PrintColor.green)
            return True
        except Exception as e:
            color_print("Exception in Queen Movement:", PrintColor.red)
            print(e)
            return False

    @staticmethod
    @Tests.register_test
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
                ]),
                 [(0,4,1,3)], True
                 ),
                (Board.start_board([# Ideal case
                ['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR'],
                ['bP', 'bP', 'bP', '##', 'bP', 'bP', 'bP', 'bP'],
                ['##', '##', '##', 'b@', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', 'bP', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR'] 
                ]),
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
                ]),
                 [(0,4,1,3)], False
                 ),
                (Board.start_board([# case where the square is attacked after eating it
                ['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR'],
                ['bP', 'bP', 'bP', 'wR', 'bP', 'bP', 'bP', 'bP'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', 'bP', '##', '##', '##', '##'],
                ['##', '##', '##', 'wR', '##', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR'] 
                ]),
                 [(0,4,1,3)], False
                 )
            ]
            
            for i, case in enumerate(cases):
                performed = True
                for movement in case[1]:
                    if not case[0].move_piece(movement[0],movement[1],movement[2],movement[3]):
                        performed = False
                        break
                    
                if performed != case[3]:
                    color_print(F"Failed Case #{i} for King Movement", PrintColor.red)
                    return False
                
            color_print("King Movement PASSED", PrintColor.green)
            return True
        except Exception as e:
            color_print("Exception in King Movement:", PrintColor.red)
            print(e)
            return False

    @staticmethod
    @Tests.register_test
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
                ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR']]),
                 [(0,4,0,2)], True
                 ),
                (Board.start_board([# case with attacked square in king's path
                ['bR', '##', '##', '##', 'b@', 'bB', 'bK', 'bR'],
                ['##', '##', '##', '##', 'bP', 'bP', 'bP', 'bP'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', 'wQ', '##', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', '##', 'w@', 'wB', 'wK', 'wR']]),
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
                ['wR', 'wK', 'wB', '##', 'w@', 'wB', 'wK', 'wR']]),
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
                ['wR', 'wK', 'wB', '##', 'w@', 'wB', 'wK', 'wR']]),
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
                ['wR', 'wK', 'wB', '##', 'w@', 'wB', 'wK', 'wR']]),
                 [(0,4,0,3),(0,3,0,1)], False
                 ),
                (Board.start_board([ # case where tower moves
                ['bR', '##', '##', '##', 'b@', 'bB', 'bK', 'bR'],
                ['##', '##', '##', '##', 'bP', 'bP', 'bP', 'bP'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['wQ', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', '##', 'w@', 'wB', 'wK', 'wR']]),
                 [(0,0,0,1),(0,1,0,0),(0,4,0,2)], False
                 ),
            ]
            
            for i, case in enumerate(cases):
                performed = True
                for movement in case[1]:
                    if not case[0].move_piece(movement[0],movement[1],movement[2],movement[3]):
                        performed = False
                        break
                    
                if performed != case[3]:
                    color_print(F"Failed Case #{i} for castling", PrintColor.red)
                    return False
                
            color_print("Castling PASSED", PrintColor.green)
            return True
        except Exception as e:
            color_print("Exception in Castling:", PrintColor.red)
            print(e)
            return False

    @staticmethod
    @Tests.register_test
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
                ]),
                 [(5,3,6,2)], False
                 )
            ]
            
            for i, case in enumerate(cases):
                performed = True
                for movement in case[1]:
                    if not case[0].move_piece(movement[0],movement[1],movement[2],movement[3]):
                        performed = False
                        break
                    
                if performed != case[3]:
                    color_print(F"Failed Case #{i} for Enpassant", PrintColor.red)
                    return False
                
            color_print("Enpassant PASSED", PrintColor.green)
            return True
        except Exception as e:
            color_print("Exception in Enpassant:", PrintColor.red)
            print(e)
            return False

    @staticmethod
    @Tests.register_test
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
                ]),
                 [(0,1,0,3)], True
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
                ]),
                 [(0,2,0,4)], False
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
                ]),
                 [(0,1,0,2),(0,2,0,4)], False
                 )
            ]
            
            for i, case in enumerate(cases):
                performed = True
                for movement in case[1]:
                    if not case[0].move_piece(movement[0],movement[1],movement[2],movement[3]):
                        performed = False
                        break
                    
                if performed != case[3]:
                    color_print(F"Failed Case #{i} for Double pawn move", PrintColor.red)
                    return False
                
            color_print("Double pawn move PASSED", PrintColor.green)
            return True
        except Exception as e:
            color_print("Exception in Double pawn move:", PrintColor.red)
            print(e)
            return False

    @staticmethod
    @Tests.register_test
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
                    
                if case[0].check != case[3]:
                    color_print(F"Failed Case #{i} for Checking", PrintColor.red)
                    return False
                
            color_print("Checking PASSED", PrintColor.green)
            return True
        except Exception as e:
            color_print("Exception in Checking:", PrintColor.red)
            print(e)
            return False

#TODO UnitTest for CheckMate

#TODO UnitTest for pawn