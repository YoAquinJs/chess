"""This module contains the grid class for handling the boards piece grid"""

from __future__ import annotations
from dataclasses import dataclass

from typing import Any, Callable, Optional

from chess_engine.piece import PIECE_STR_LENGTH, Piece, SideColor
from chess_engine.structs import Coord
from serialization.serializable import Serializable
from utils.exceptions import InvalidGridError

# Constants for board
ROWS    = ['8','7','6','5','4','3','2','1']
COLUMNS = ['a','b','c','d','e','f','g','h']
BOARD_START = [
    ['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR'], # 8
    ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'], # 7
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '], # 6
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '], # 5
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '], # 4
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '], # 3
    ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'], # 2
    ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR']  # 1
]#    a     b     c     d      e     f     g     h

class Grid(Serializable):
    """TODO
    """

    def __init__(self, grid: list[list[Optional[Piece]]]) -> None:
        if len(grid) != len(ROWS):
            raise InvalidGridError("Invalid row count")
        for column in grid:
            if len(column) != len(COLUMNS):
                raise InvalidGridError("Invalid column count")

        self.__grid = grid
        self.white_pieces: set[Piece]
        self.black_pieces: set[Piece]
        self._set_piece_lists()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Grid):
            return False

        for piece, coord in GridIter(self):
            if other.get_at(coord) != piece:
                return False

        return True

    def get_at(self, coord: Coord) -> Optional[Piece]:
        """TODO
        """
        return self.__grid[coord.row][coord.column]

    def set_at(self, coord: Coord, piece: Optional[Piece]) -> Optional[Piece]:
        """Sets the grid coordinate to the given piece, and return whatever was contained

        Args:
            coord (Coord): Coordinate
            piece (Optional[Piece]): The piece to set or None for emptying the coordinate

        Returns:
            Optional[Piece]: Previous piece in the coordinate or None if it was empty
        """
        prev_piece = self._set_at(coord, piece)
        self._set_piece_lists()
        return prev_piece

    def _set_at(self, coord: Coord, piece: Optional[Piece]) -> Optional[Piece]:
        prev_piece = self.__grid[coord.row][coord.column]
        self.__grid[coord.row][coord.column] = piece
        return prev_piece

    def _set_piece_lists(self) -> None:
        def add_possible(piece: Optional[Piece]) -> None:
            if not isinstance(piece, Piece):
                return
            if piece.color == SideColor.WHITE:
                self.white_pieces.add(piece)
            if piece.color == SideColor.BLACK:
                self.black_pieces.add(piece)

        self.white_pieces = set()
        self.black_pieces = set()
        for piece, _ in GridIter(self):
            add_possible(piece)

    def swap_pieces(self, coord1: Coord, coord2: Coord) -> None:
        """Swaps the pieces in the given coordinates

        Args:
            coord1 (Coord): Coordinate 1
            coord2 (Coord): Coordinate 2
        """
        piece1 = self.get_at(coord1)
        if piece1 is not None:
            piece1.coord = coord2
        piece2 = self.get_at(coord1)
        if piece2 is not None:
            piece2.coord = coord1

        self.set_at(coord1, piece2)
        self.set_at(coord2, piece1)

    def print_grid(self) -> None:
        """TODO
        """
        for column in COLUMNS:
            print(f"  {column}", end="")

        print()
        for piece, _ in GridIter(self, on_new_row=lambda r : print(ROWS[r])):
            piece_str = " "*PIECE_STR_LENGTH if piece is None else str(piece)
            print(f" {piece_str} ", end="")

    @staticmethod
    def get_start_grid() -> Grid:
        """TODO
        """
        return Grid.from_str_grid(BOARD_START)

    @staticmethod
    def from_str_grid(text_grid: list[list[str]]) -> Grid:
        """TODO
        """
        if len(text_grid) != len(ROWS) or len(text_grid[0]) != len(COLUMNS):
            raise ValueError("Text grid must have the same lengths as the \
                            'ROWS' and 'COLUMNS' constants")

        grid: list[list[Optional[Piece]]] = []
        for r, row in enumerate(text_grid):
            grid.append([])
            for c, piece_str in enumerate(row):
                grid[r].append(Piece.parse_from_str(piece_str, Coord(r, c)))
        return Grid(grid)

    def get_serialization_attrs(self) -> dict[str, Any]:
        text_grid: list[list[str]] = []
        for piece, coord in GridIter(self, lambda _: text_grid.append([])):
            piece_str = " "*PIECE_STR_LENGTH if piece is None else str(piece)
            text_grid[coord.row].append(piece_str)
        return {
            "grid": text_grid
        }

    @classmethod
    def get_from_deserialize(cls, attrs: dict[str, Any], **kwargs: Any) -> Grid:
        """TODO
        """
        return Grid.from_str_grid(attrs["grid"])


@dataclass
class GridIter:
    """TODO
    """

    grid: Grid
    row = 0
    col = 0
    on_new_row: Callable[[int], None] = lambda _: None

    def __post_init__(self) -> None:
        self.on_new_row(self.row)

    def __iter__(self) -> GridIter:
        return self

    def __next__(self) -> tuple[Optional[Piece], Coord]:
        if self.row >= len(ROWS):
            raise StopIteration
        if self.col >= len(COLUMNS):
            self.on_new_row(self.row)
            self.row += 1
            self.col = 0
            return next(self)
        self.col += 1
        coord = Coord(self.row, self.col)
        return self.grid.get_at(coord), coord
