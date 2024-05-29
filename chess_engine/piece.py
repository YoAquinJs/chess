"""This module contains the Piece model object and it's properties"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import cast

from chess_engine.enums import MovSpecialCase, PieceType, SideColor
from chess_engine.structs import Coord, Dir
from utils.errors import EnumParseError

BLACK_MOV_DIR = 1
WHITE_MOV_DIR = -1

PIECE_STR_LENGTH = 2
NULL_PIECE_STR = " "*PIECE_STR_LENGTH

SerPiece = tuple[str, tuple[int,int]]

@dataclass
class Piece():
    """TODO
    """
    type: PieceType
    color: SideColor
    coord: Coord
    movements: dict[Dir, MovSpecialCase]= field(init=False)

    def __post_init__(self) -> None:
        moving_dir = WHITE_MOV_DIR if self.color == SideColor.WHITE else BLACK_MOV_DIR
        self.movements = Piece.get_type_movements(self.type, moving_dir)

    def __str__(self) -> str:
        piece_str = f"{self.color.value}{self.type.value}"
        if len(piece_str) != PIECE_STR_LENGTH:
            raise ValueError(f"String format of piece must have {PIECE_STR_LENGTH} characters")
        return piece_str

    def __hash__(self) -> int:
        """Hash on type, color and coordinate"""
        return hash((self.type, self.color, self.coord.row, self.coord.column))

    def __eq__(self, other: object) -> bool:
        """Equality on type, color and coordinate"""
        if not isinstance(other, Piece):
            return False

        return hash(self) == hash(other)

    def __ne__(self, other: object) -> bool:
        return not self == other

    def same_as(self, other: object) -> bool:
        """TODO
        """
        if not isinstance(other, Piece):
            return False

        return (self.type, self.color) == (other.type, other.color)

    def can_extend(self) -> bool:
        """Get whether the piece has or not extendable movement

        Args:
            piece_type (PieceType): Type to determine from

        Returns:
            bool: Extendable
        """
        return self.type not in (PieceType.PAWN, PieceType.KING)

    @staticmethod
    def get_type_movements(piece_type: PieceType, mov_dir: int=0) -> dict[Dir, MovSpecialCase]:
        """TODO
        """
        match piece_type:
            case PieceType.PAWN:
                return {
                    Dir(1 * mov_dir,0)  : MovSpecialCase.PAWN_MOVE,
                    Dir(1 * mov_dir,-1) : MovSpecialCase.PAWN_ATTACK,
                    Dir(1 * mov_dir,1)  : MovSpecialCase.PAWN_ATTACK,
                    Dir(2 * mov_dir,0)  : MovSpecialCase.DOUBLE_PAWN_MOVE
                }
            case PieceType.BISHOP:
                return {
                    Dir(1,1)   : MovSpecialCase.NONE,
                    Dir(-1,1)  : MovSpecialCase.NONE,
                    Dir(1,-1)  : MovSpecialCase.NONE,
                    Dir(-1,-1) : MovSpecialCase.NONE,
                }
            case PieceType.KNIGTH:
                return {
                    Dir(1, 2)  : MovSpecialCase.NONE,
                    Dir(2, 1)  : MovSpecialCase.NONE,
                    Dir(2, -1) : MovSpecialCase.NONE,
                    Dir(1, -2) : MovSpecialCase.NONE,
                    Dir(-1,-2) : MovSpecialCase.NONE,
                    Dir(-2,-1) : MovSpecialCase.NONE,
                    Dir(-2,1)  : MovSpecialCase.NONE,
                    Dir(-1,2)  : MovSpecialCase.NONE,
                }
            case PieceType.ROOK:
                return {
                    Dir(1,0)   : MovSpecialCase.NONE,
                    Dir(-1,0)  : MovSpecialCase.NONE,
                    Dir(0,1)   : MovSpecialCase.NONE,
                    Dir(0,-1)  : MovSpecialCase.NONE,
                }
            case PieceType.QUEEN:
                return {
                    Dir(1,1)   : MovSpecialCase.NONE,
                    Dir(-1,1)  : MovSpecialCase.NONE,
                    Dir(1, -1) : MovSpecialCase.NONE,
                    Dir(-1,-1) : MovSpecialCase.NONE,
                    Dir(1,0)   : MovSpecialCase.NONE,
                    Dir(-1,0)  : MovSpecialCase.NONE,
                    Dir(0,1)   : MovSpecialCase.NONE,
                    Dir(0,-1)  : MovSpecialCase.NONE,
                }
            case PieceType.KING:
                return {
                    Dir(1,0)   : MovSpecialCase.NONE,
                    Dir(-1,0)  : MovSpecialCase.NONE,
                    Dir(0,1)   : MovSpecialCase.NONE,
                    Dir(0,-1)  : MovSpecialCase.NONE,
                    Dir(-1, 1) : MovSpecialCase.NONE,
                    Dir(1,-1)  : MovSpecialCase.NONE,
                    Dir(1,1)   : MovSpecialCase.NONE,
                    Dir(-1,-1) : MovSpecialCase.NONE,
                    Dir(0,-2)  : MovSpecialCase.CASTLE,
                    Dir(0,2)   : MovSpecialCase.CASTLE
                }

    @staticmethod
    def from_str(piece_str: str, coord: Coord) -> OptPiece:
        """TODO
        """
        if len(piece_str) != PIECE_STR_LENGTH:
            raise ValueError(f"The parsed string must contain {PIECE_STR_LENGTH} characters")

        try:
            color = cast(SideColor, SideColor[piece_str[0]])
            piece_type = cast(PieceType, PieceType[piece_str[1]])
            return Piece(piece_type, color, coord)
        except EnumParseError:
            return None

    @staticmethod
    def get_str(piece: OptPiece) -> str:
        """TODO
        """
        return NULL_PIECE_STR if piece is None else str(piece)

    @staticmethod
    def serialize(piece: Piece) -> SerPiece:
        """TODO
        """
        return (str(piece), piece.coord.to_tupple())

    @staticmethod
    def deserialize(ser: SerPiece) -> OptPiece:
        """TODO
        """
        return Piece.from_str(ser[0], Coord(*ser[1]))

OptPiece = Piece | None
