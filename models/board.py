from typing import Dict

from models.consts import COLUMNS, ROWS, BOARD_START, PieceType, PlayerColor
from models.piece import Piece

class Board():
    """Class for handling game screens, and game states

    Attributes:
        matrix (Dict[str, Dict[str, Piece]]): Matrix representing the board configuration
    """

    def __init__(self, matrix: Dict[str, Dict[str, Piece]]) -> None:
        self.matrix = matrix
        self.rows = ROWS
        self.columns = COLUMNS
        
        self.whitePieces = []
        self.blackPieces = []
        
        for row in ROWS:
            for column in COLUMNS:
                piece = self.matrix[row][column]
                if piece.type != PieceType.empty:
                    self.whitePieces.append(piece) if piece.color == PlayerColor.white else self.blackPieces.append(piece)
                
    @classmethod
    def start_board(cls) -> object:
        matrix = {}
        for row in ROWS:
            matrix[row] = {}
            for column in COLUMNS:
                piece = BOARD_START[row][column]
                matrix[row][column] = Piece(PieceType[piece[0]], PlayerColor[piece[1]], row, column) if PieceType[piece[0]] != PieceType.empty else Piece.empty()
                
        return cls(matrix)