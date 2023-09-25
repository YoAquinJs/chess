 #//from typing import Dict

from models.consts import PieceType, PlayerColor, MovementSpecialCase, BLACK_MOV_DIR, WHITE_MOV_DIR#//, COLUMNS, ROWS, BOARD_START

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
        self.movingDir = WHITE_MOV_DIR if self.color == PlayerColor.white else BLACK_MOV_DIR
        
        # Direction (column direction, (x movement), row direction (y movement))
        if self.type == PieceType.pawn:
            """
            _ _ # _ _
            _ # # # _
            _ _ P _ _
            _ _ _ _ _
            _ _ _ _ _
            """
            self.moved = False
            self.extendMovement = False
            self.posibleMovements = {
                (0, 1 * self.movingDir) : [],#TODO check that isn't enemy either
                (-1, 1 * self.movingDir) : [MovementSpecialCase.isEnemy, MovementSpecialCase.enPassant],
                (1, 1 * self.movingDir) : [MovementSpecialCase.isEnemy, MovementSpecialCase.enPassant],
                (0, 2 * self.movingDir) : [MovementSpecialCase.doublePawnMove]
                }
        elif self.type == PieceType.bishop:
            """
            # _ _ _ #
            _ # _ # _
            _ _ B _ _
            _ # _ # _
            # _ _ _ #
            """
            self.extendMovement = True
            self.posibleMovements = {
                (1, 1) : [],
                (-1, 1) : [],
                (1, -1) : [],
                (-1, -1) : [],
                }
        elif self.type == PieceType.knigth:
            """
            _ # _ # _
            # _ _ _ #
            _ _ K _ _
            # _ _ _ #
            _ # _ # _
            """
            self.extendMovement = False
            self.posibleMovements = {
                (1, 2) : [],
                (2, 1) : [],
                (2, -1) : [],
                (1, -2) : [],
                (-1, -2) : [],
                (-2, -1) : [],
                (-2, 1) : [],
                (-1, 2) : [],
                }
        elif self.type == PieceType.rook:
            """
            _ _ # _ _
            _ _ # _ _
            # # R # #
            _ _ # _ _
            _ _ # _ _
            """
            self.extendMovement = True
            self.posibleMovements = {
                (1, 0) : [],
                (-1, 0) : [],
                (0, 1) : [],
                (0, -1) : [],
                }
        elif self.type == PieceType.queen:
            """
            # _ # _ #
            _ # # # _
            # # Q # #
            _ # # # _
            # _ # _ #
            """
            self.extendMovement = True
            self.posibleMovements = {
                (1, 1) : [],
                (-1, 1) : [],
                (1, -1) : [],
                (-1, -1) : [],
                (1, 0) : [],
                (-1, 0) : [],
                (0, 1) : [],
                (0, -1) : [],
                }
        elif self.type == PieceType.king:
            """
            _ _ _ _ _
            _ _ # _ _
            _ # @ # _
            _ _ # _ _
            _ _ _ _ _
            """
            self.extendMovement = False
            self.posibleMovements = {
                (1, 0) : [],
                (-1, 0) : [],
                (0, 1) : [],
                (0, -1) : [],
                }

    
    #//@classmethod
    #//def empty(cls) -> object:
    #//    return cls(PieceType.empty, None, str(), str())
    