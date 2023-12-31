"""This module contains the Piece model object and it's properties"""

# Import Internal module
from core.consts import PieceType, PlayerColor, MovementSpecialCase, BLACK_MOV_DIR, WHITE_MOV_DIR, PLAYERCOLORINT, PIECETYPEINT

class Piece():
    """Class for handling game screens, and game states

    Attributes:
        type (PieceType): The type of piece
        color (PlayerColor): The color of the piece
        row (int): The row of the piece
        column (int): The column of the piece
        maxExtend (int): The max number of extendable movement posible.
        posibleMovements (Dict[Union[int, int], MovementSpecialCase])
        movingDirection (int): The movement direction of the piece (Pawn only, up or down the board depending in playercolor).
    """

    def __init__(self, type: PieceType, color: PlayerColor, row: int, column: int) -> None:
        """Returns a font object

        Args:
            type (PieceType): Piece type.
            color (PlayerColor): Piece color.
            row (int): Piece row.
            column (int): Piece column
        """

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
            _ # # # _
            # # @ # #
            _ # # # _
            _ _ _ _ _
            """
            self.maxExtend = 1
            self.posibleMovements = {
                (1, 0) : None,
                (-1, 0) : None,
                (0, 1) : None,
                (0, -1) : None,
                (-1, 1) : None,
                (1, -1) : None,
                (1, 1) : None,
                (-1, -1) : None,
                (0,-2) : MovementSpecialCase.castle,
                (0,2) : MovementSpecialCase.castle
                }

    #! Development only function
    def print_piece(self):
        print(self.color, self.type, (self.row, self.column))

    def __str__(self):
        return f"{self.color.value}{self.type.value}"
    
    def __hash__(self) -> int:
        return id(self)#int((PLAYERCOLORINT[self.color]*1000)+(PIECETYPEINT[self.type]*100)+((self.row+1)*10)+((self.column+1)*1))

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()
    #//@classmethod
    #//def empty(cls) -> object:
    #//    return cls(PieceType.empty, None, str(), str())
    