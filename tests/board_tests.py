"""This module contain unit tests for the board class functionalities"""

# Import external libraries
import traceback
from copy import deepcopy

# Import Internal modules
from tests.tests import Tests
from chess_engine.board import Board
from game_logic.consts import PrintColor, PlayerColor, PieceType, TestType, BoardState, BOARD_START, ROWS, COLUMNS
from utils.utils import color_print

class BoardTests():
    """Test class containing Unit tests for the board Class functionalities"""
    
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
        """Test for validating the board serialization

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
            cases = []
            board = Board.start_board()
            cases.append((list(set(item for sublist in deepcopy(board.blackPieces).values() for item in sublist)),
                         [(2,0),(2,1),(2,2),(2,3),(2,4),(2,5),(2,6),(2,7)]))
            board = Board.start_board(turn=PlayerColor.black)
            cases.append((list(set(item for sublist in deepcopy(board.whitePieces).values() for item in sublist)),
                         [(5,0),(5,1),(5,2),(5,3),(5,4),(5,5),(5,6),(5,7)]))
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
            cases.append((list(set(item for sublist in deepcopy(board.blackPieces).values() for item in sublist)),
                         [(1,0),(2,1),(3,1),(2,2),(4,2),(1,3),(2,3),(2,4),(4,4),(2,5),(3,5),(2,6),(4,6),(2,7),(5,7)]))
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
            cases.append((list(set(item for sublist in deepcopy(board.blackPieces).values() for item in sublist)),
                         [(1,0),(0,1),(2,1),(3,1),(2,2),(4,2),(1,3),(2,3),(2,4),(4,4),(2,5),(3,5),(2,6),(4,6),(2,7),(5,7),(5,3),(6,2),(6,0)]))
            
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
                ['##', '##', '##', 'bP', '##', '##', '##', '##'],
                ['##', 'wB', '##', '##', '##', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR'] 
                ]),
                 [(5,1,4,0)], True
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
                 )
            ]
            
            for i, case in enumerate(cases):
                for movement in case[1]:
                    if not case[0].attempt_move(movement[0],movement[1],movement[2],movement[3])[0]:
                        color_print(f"Movement not performed {movement}, in Case #{i}", PrintColor.yellow)
                        break
                    
                if (case[0].boardState == BoardState.check or case[0].boardState == BoardState.checkmate) != case[2]:
                    color_print(F"Failed Case #{i} for Checking in turn {case[0].turn}, {case[0].boardState}", PrintColor.red)
                    return False
                
            color_print("Checking PASSED", PrintColor.green)
            return True
        except Exception as e:
            color_print("Exception in Checking:", PrintColor.red)
            print(e)
            traceback.print_exc()
            return False

    @staticmethod
    @Tests.register_test(TestType.board)    
    def checkmating() -> bool:
        """Test for validating the checkmate algorithm

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
                ['##', '##', '##', 'bP', '##', '##', '##', '##'],
                ['##', 'wB', '##', '##', '##', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR'] 
                ]),
                 [(5,1,4,0)], False
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
                 [(5,4,1,4)], False
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
                 ),
                (Board.start_board([
                ['bR', 'bB', 'bK', 'bB', 'b@', 'bB', 'bK', 'bR'],
                ['bP', '##', '##', '##', 'bP', 'bP', 'bP', 'bP'],
                ['##', 'bP', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', '##', '##', '##', '##', '##'],
                ['##', '##', '##', 'bP', 'wB', '##', '##', '##'],
                ['##', '##', '##', '##', 'wQ', '##', '##', '##'],
                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                ['wR', 'wK', 'wB', 'wQ', 'w@', '##', 'wK', 'wR'] 
                ]),
                 [(4,4,2,2)], True
                 )
            ]
            
            for i, case in enumerate(cases):
                for movement in case[1]:
                    if not case[0].attempt_move(movement[0],movement[1],movement[2],movement[3])[0]:
                        color_print(f"Movement not performed {movement}, in Case #{i}", PrintColor.yellow)
                        break
                    
                    if (case[0].boardState == BoardState.checkmate) != case[2]:
                        playerPieces = case[0].whitePieces if case[0].turn == PlayerColor.white else case[0].blackPieces
                        print([(p.type, p.color, (p.row,p.column), movs) for p, movs in playerPieces.items()])
                        color_print(F"Failed Case #{i} for checkmating in turn {case[0].turn}, {case[0].boardState}", PrintColor.red)
                        return False
                
            color_print("Checkmating PASSED", PrintColor.green)
            return True
        except Exception as e:
            color_print("Exception in Checkmating:", PrintColor.red)
            print(e)
            traceback.print_exc()
            return False
