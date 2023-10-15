"""This module contains the Piece model object and it's properties"""

from models.consts import PieceType, PlayerColor, MovementSpecialCase, BLACK_MOV_DIR, WHITE_MOV_DIR#//, COLUMNS, ROWS, BOARD_START

class Piece():
    """Class for handling game screens, and game states

    Attributes:
        type (PieceType): The type of piece
        color (PlayerColor): The color of the piece
        row (int): The row of the piece
        column (int): The column of the piece
    """

    def __init__(self, type: PieceType, color: PlayerColor, row: int, column: int) -> None:
        self.type = type
        self.color = color
        self.row = row
        self.column = column
        
        self.maxExtend = 8 # Meaning the piece can move without a limit
        self.posibleMovements = None
        self.movingDirection = WHITE_MOV_DIR if self.color == PlayerColor.white else BLACK_MOV_DIR
        
        # Direction (column direction, (x movement), row direction (y movement))
        if self.type == PieceType.pawn:
            """
            _ _ # _ _
            _ # # # _
            _ _ P _ _
            _ _ _ _ _
            _ _ _ _ _
            """
            self.maxExtend = 1
            self.posibleMovements = {
                (1 * self.movingDirection,0) : MovementSpecialCase.isEmpty,
                (1 * self.movingDirection,-1) : None,
                (1 * self.movingDirection,1) : None,
                (2 * self.movingDirection,0) : MovementSpecialCase.doublePawnMove
                }
        elif self.type == PieceType.bishop:
            """
            # _ _ _ #
            _ # _ # _
            _ _ B _ _
            _ # _ # _
            # _ _ _ #
            """
            self.posibleMovements = {
                (1, 1) : None,
                (-1, 1) : None,
                (1, -1) : None,
                (-1, -1) : None,
                }
        elif self.type == PieceType.knigth:
            """
            _ # _ # _
            # _ _ _ #
            _ _ K _ _
            # _ _ _ #
            _ # _ # _
            """
            self.maxExtend = 1
            self.posibleMovements = {
                (1, 2) : None,
                (2, 1) : None,
                (2, -1) : None,
                (1, -2) : None,
                (-1, -2) : None,
                (-2, -1) : None,
                (-2, 1) : None,
                (-1, 2) : None,
                }
        elif self.type == PieceType.rook:
            """
            _ _ # _ _
            _ _ # _ _
            # # R # #
            _ _ # _ _
            _ _ # _ _
            """
            self.posibleMovements = {
                (1, 0) : None,
                (-1, 0) : None,
                (0, 1) : None,
                (0, -1) : None,
                }
        elif self.type == PieceType.queen:
            """
            # _ # _ #
            _ # # # _
            # # Q # #
            _ # # # _
            # _ # _ #
            """
            self.posibleMovements = {
                (1, 1) : None,
                (-1, 1) : None,
                (1, -1) : None,
                (-1, -1) : None,
                (1, 0) : None,
                (-1, 0) : None,
                (0, 1) : None,
                (0, -1) : None,
                }
        elif self.type == PieceType.king:
            """
            _ _ _ _ _
            _ _ # _ _
            # # @ # #
            _ _ # _ _
            _ _ _ _ _
            """
            self.maxExtend = 1
            self.posibleMovements = {
                (1, 0) : None,
                (-1, 0) : None,
                (0, 1) : None,
                (0, -1) : None,
                (0,-2) : MovementSpecialCase.canCastle,
                (0,2) : MovementSpecialCase.canCastle
                }

    def __str__(self):
        return f"{self.color.value}{self.type.value}"
    #//@classmethod
    #//def empty(cls) -> object:
    #//    return cls(PieceType.empty, None, str(), str())
    