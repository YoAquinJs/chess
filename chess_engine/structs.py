"""This module contains the coordinate class representation"""

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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Coord):
            return False
        return self.row == other.row and self.column == other.column

class Dir(NamedTuple):
    """Represents a direction

    Attributes:
        x (int): X.
        y (int): Y.
    """

    x: int
    y: int

    def to_tupple(self) -> tuple[int, int]:
        """TODO
        """
        return (self.x, self.y)

class CastlingState(NamedTuple):
    """Represents the castling state of a player

    Attributes:
        leff (bool): Left castle state.
        right (int): Right castle state.
    """

    left: bool
    right: bool
