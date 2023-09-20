from typing import Dict

from models.consts import COLUMNS, ROWS, BOARD_START, PieceType, PlayerColor

class Piece():
    """Class for handling game screens, and game states

    Attributes:
        type (PieceType): The type of piece
        color (PlayerColor): The color of the piece
        row (str): The row of the piece
        column (str): The column of the piece
        kingLocked (bool, Optional): Is true, if at the moment the piece is moved, the king is checked. Defaults to False
    """

    def __init__(self, type: PieceType, color: PlayerColor, row: str, column: str, kingLocked: bool = False) -> None:
        self.type = type
        self.color = color
        self.row = row
        self.column = column
        
        self.kingLocked = kingLocked
        
    @classmethod
    def empty(cls) -> object:
        return cls(PieceType.empty, None, str(), str())
    