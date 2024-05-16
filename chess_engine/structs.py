"""This module contains the coordinate class representation"""

from __future__ import annotations

from math import copysign
from typing import NamedTuple


class Coord(NamedTuple):
    """Represents a coordinate

    Attributes:
        row (int): Row.
        column (int): Column.
    """

    row: int
    column: int

    def to_tupple(self) -> tuple[int, int]:
        """TODO
        """
        return (self.row, self.column)

    def get_dir_to(self, other: Coord) -> Dir:
        """TODO
        """
        return Dir(other.row-self.row, other.column-self.column)

    def to_dir(self, direction: Dir, factor: int=1) -> Coord:
        """TODO
        """
        return Coord(self.row+(direction.row*factor), self.column+(direction.column*factor))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Coord):
            return False
        return self.row == other.row and self.column == other.column

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, Coord):
            return True
        return self.row != other.row or self.column != other.column

class Dir(NamedTuple):
    """Represents a direction

    Attributes:
        x (int): X.
        y (int): Y.
    """

    row: int
    column: int

    def normalized(self) -> Dir:
        """TODO
        """
        if self.row != 0 and self.column != 0 and self.row != self.column:
            return self
        row = 0 if self.row == 0 else int(copysign(1, self.row))
        column = 0 if self.column == 0 else int(copysign(1, self.column))
        return Dir(row, column)

    def to_tupple(self) -> tuple[int, int]:
        """TODO
        """
        return (self.row, self.column)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Dir):
            return False
        return self.row == other.row and self.column == other.column

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, Dir):
            return True
        return self.row != other.row or self.column != other.column

    def __hash__(self) -> int:
        return hash((self.row, self.column))

class CastlingState(NamedTuple):
    """Represents the castling state of a player

    Attributes:
        leff (bool): Left castle state.
        right (int): Right castle state.
    """

    left: bool
    right: bool
