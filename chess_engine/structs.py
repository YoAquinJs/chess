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
