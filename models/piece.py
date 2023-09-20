 #//from typing import Dict

from models.consts import PieceType, PlayerColor#//, COLUMNS, ROWS, BOARD_START

class Piece():
    """Class for handling game screens, and game states

    Attributes:
        type (PieceType): The type of piece
        color (PlayerColor): The color of the piece
        row (int): The row of the piece
        column (int): The column of the piece
        kingLocked (bool, Optional): Is true, if at the moment the piece is moved, the king is checked. Defaults to False
    """

    def __init__(self, type: PieceType, color: PlayerColor, row: int, column: int, kingLocked: bool = False) -> None:
        self.type = type
        self.color = color
        self.row = row
        self.column = column
        
        self.kingLocked = kingLocked
        
        if self.type == PieceType.pawn:
            self.extendMovement = False
        elif self.type == PieceType.bishop:
            self.extendMovement = True
        elif self.type == PieceType.knigth:
            self.extendMovement = False
        elif self.type == PieceType.rook:
            self.extendMovement = True
        elif self.type == PieceType.queen:
            self.extendMovement = True
        elif self.type == PieceType.king:
            self.extendMovement = False
        
    #//@classmethod
    #//def empty(cls) -> object:
    #//    return cls(PieceType.empty, None, str(), str())
    