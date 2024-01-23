"""This module contains the Piece model object and it's properties"""

from __future__ import annotations

from game_logic.consts import MovSpecialCase, PieceType, PlayerColor, BLACK_MOV_DIR, WHITE_MOV_DIR


#TODO refactor for readability
class Piece():
    """TODO
    """

    def __init__(self, piece_type: PieceType, color: PlayerColor, row: int, column: int) -> None:
        self.type = piece_type
        self.color = color
        self.row = row
        self.column = column

        self.max_extend = 8 # Meaning the piece can move without a limit
        self.posible_movs = None
        self.moving_dir = WHITE_MOV_DIR if self.color == PlayerColor.WHITE else BLACK_MOV_DIR

        # Direction (column direction, (x movement), row direction (y movement))
        if self.type == PieceType.PAWN:
            self.max_extend = 1
            self.posible_movs = {
                (1 * self.moving_dir,0) : MovSpecialCase.IS_EMPTY,
                (1 * self.moving_dir,-1) : None,
                (1 * self.moving_dir,1) : None,
                (2 * self.moving_dir,0) : MovSpecialCase.DOUBLE_PAWN_MOVE
                }
        elif self.type == PieceType.BISHOP:
            self.posible_movs = {
                (1, 1) : None,
                (-1, 1) : None,
                (1, -1) : None,
                (-1, -1) : None,
                }
        elif self.type == PieceType.KNIGTH:
            self.max_extend = 1
            self.posible_movs = {
                (1, 2) : None,
                (2, 1) : None,
                (2, -1) : None,
                (1, -2) : None,
                (-1, -2) : None,
                (-2, -1) : None,
                (-2, 1) : None,
                (-1, 2) : None,
                }
        elif self.type == PieceType.ROOK:
            self.posible_movs = {
                (1, 0) : None,
                (-1, 0) : None,
                (0, 1) : None,
                (0, -1) : None,
                }
        elif self.type == PieceType.QUEEN:
            self.posible_movs = {
                (1, 1) : None,
                (-1, 1) : None,
                (1, -1) : None,
                (-1, -1) : None,
                (1, 0) : None,
                (-1, 0) : None,
                (0, 1) : None,
                (0, -1) : None,
                }
        elif self.type == PieceType.KING:
            self.max_extend = 1
            self.posible_movs = {
                (1, 0) : None,
                (-1, 0) : None,
                (0, 1) : None,
                (0, -1) : None,
                (-1, 1) : None,
                (1, -1) : None,
                (1, 1) : None,
                (-1, -1) : None,
                (0,-2) : MovSpecialCase.CASTLE,
                (0,2) : MovSpecialCase.CASTLE
                }

    #! Development only function
#    def print_piece(self) -> None:
#        print(self.color, self.type, (self.row, self.column))

    def __str__(self) -> str:
        return f"{self.color.value}{self.type.value}"

    def __hash__(self) -> int:
        return id(self)

    def __eq__(self, other: object) -> bool:
        return self.__hash__() == other.__hash__()
