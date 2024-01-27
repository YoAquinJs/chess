"""This module contains the Piece model object and it's properties"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, cast

from chess_engine.structs import Coord, Dir
from utils.exceptions import EnumParseError
from utils.parseable_enum import ParseableEnum


class SideColor(Enum, metaclass=ParseableEnum):
    """Enum for piece color
    """
    WHITE = 'w'
    BLACK = 'b'

class PieceType(Enum, metaclass=ParseableEnum):
    """Enum for each type of piece
    """
    PAWN = 'P'
    BISHOP = 'B'
    KNIGTH = 'K'
    ROOK = 'R'
    QUEEN = 'Q'
    KING = '@'

class MovSpecialCase(Enum):
    """Enum for each type of piece
    """
    NONE = auto()
    CASTLE = auto()
    DOUBLE_PAWN_MOVE = auto()
    IS_EMPTY = auto()

BLACK_MOV_DIR = 1
WHITE_MOV_DIR = -1

PIECE_STR_LENGTH = 2

SerPiece = tuple[str, tuple[int,int]]
@dataclass
class Piece():
    """TODO
    """
    type: PieceType
    color: SideColor
    coord: Coord
    moving_dir: int = field(init=False)
    extendable_mov: bool = field(init=False)
    movements: dict[Dir, MovSpecialCase]= field(init=False)

    def __post_init__(self) -> None:
        self.moving_dir = WHITE_MOV_DIR if self.color == SideColor.WHITE else BLACK_MOV_DIR
        if self.moving_dir not in (1, -1):
            raise ValueError("The movement direction of the piece can only be 1 or -1")
        self.extendable_mov = Piece.get_extendability(self.type)
        self.movements = Piece.get_type_movements(self.type, self.moving_dir)

    def __str__(self) -> str:
        piece_str = f"{self.color.value}{self.type.value}"
        if len(piece_str) != PIECE_STR_LENGTH:
            raise ValueError(f"String format of piece must have {PIECE_STR_LENGTH} characters")
        return piece_str

    def __hash__(self) -> int:
        return id(self)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Piece):
            return False

        if self.type != other.type:
            return False
        if self.color != other.color:
            return False
        if self.coord != other.coord:
            return False
        return True

    @staticmethod
    def get_extendability(piece_type: PieceType) -> bool:
        """Get whether the piece has or not extendable movement

        Args:
            piece_type (PieceType): Type to determine from

        Returns:
            bool: Extendable
        """
        return piece_type not in (PieceType.PAWN, PieceType.KING)

    @staticmethod
    def get_type_movements(piece_type: PieceType, mov_dir: int=0) -> dict[Dir, MovSpecialCase]:
        """Provides the corresponding movements to the piece type

        Args:
            piece_type (PieceType): Type to determine from
            mov_dir (int, optional): Piece movement direction depending on color. Defaults to 0.

        Returns:
            dict[Dir, Optional[MovSpecialCase]]: Movements
        """
        match piece_type:
            case PieceType.PAWN:
                return {
                Dir(1 * mov_dir,0)  : MovSpecialCase.IS_EMPTY,
                Dir(1 * mov_dir,-1) : MovSpecialCase.NONE,
                Dir(1 * mov_dir,1)  : MovSpecialCase.NONE,
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

    def serialize(self) -> SerPiece:
        """TODO
        """
        return (str(self), self.coord.to_tupple())

    @staticmethod
    def deserialize(ser: SerPiece) -> Optional[Piece]:
        """TODO
        """
        return Piece.parse_from_str(ser[0], Coord(*ser[1]))

    @staticmethod
    def parse_from_str(piece_str: str, coord: Coord) -> Optional[Piece]:
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
