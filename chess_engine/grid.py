"""This module contains the grid class for handling the boards piece grid"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from chess_engine.piece import Piece, SideColor, OptPiece
from chess_engine.structs import Coord
from serialization.serializable import Serializable
from utils.exceptions import GridInvalidCoordError, InvalidGridError

# Constants for board
ROWS    = ['8','7','6','5','4','3','2','1']
COLUMNS = ['a','b','c','d','e','f','g','h']
L_ROWS = len(ROWS)
L_COLUMNS = len(COLUMNS)
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

    def __init__(self, grid: list[list[OptPiece]]) -> None:
        if len(grid) != len(ROWS):
            raise InvalidGridError("Invalid row count")
        for column in grid:
            if len(column) != len(COLUMNS):
                raise InvalidGridError("Invalid column count")

        self.__grid = grid

        for piece, coord in GridIter(self):
            if piece is not None and piece.coord != coord:
                error_msg = f"Piece's coord does not match coord in grid, Piece: {piece}"
                raise InvalidGridError(error_msg)

        self.white_pieces: set[Piece]
        self.black_pieces: set[Piece]
        self._categorize_lists()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Grid):
            return False

        for piece, coord in GridIter(self):
            if other.get_at(coord) != piece:
                return False

        return True

    def get_at(self, coord: Coord) -> OptPiece:
        """TODO
        """
        if coord.row < 0 or coord.row >= L_ROWS or coord.column < 0 or coord.column >= L_COLUMNS:
            raise GridInvalidCoordError
        return self.__grid[coord.row][coord.column]

    def set_at(self, coord: Coord, piece: OptPiece) -> OptPiece:
        """Sets the grid coordinate to the given piece, and return whatever was contained

        Args:
            coord (Coord): Coordinate
            piece (OptPiece): The piece to set or None for emptying the coordinate

        Returns:
            OptPiece: Previous piece in the coordinate or None if it was empty
        """
        prev_piece = self._set_at(coord, piece)
        self._categorize_lists()
        return prev_piece

    def _set_at(self, coord: Coord, piece: OptPiece) -> OptPiece:
        if piece is not None:
            piece.coord = coord
        prev_piece = self.get_at(coord)
        self.__grid[coord.row][coord.column] = piece
        return prev_piece

    def swap_pieces(self, coord1: Coord, coord2: Coord) -> None:
        """Swaps the pieces in the given coordinates

        Args:
            coord1 (Coord): Coordinate 1
            coord2 (Coord): Coordinate 2
        """
        if coord1 == coord2:
            raise GridInvalidCoordError

        piece1 = self._set_at(coord1, self.get_at(coord2))
        self._set_at(coord2, piece1)

    def _categorize_lists(self) -> None:
        self.white_pieces = set()
        self.black_pieces = set()
        for piece, _ in GridIter(self):
            if not isinstance(piece, Piece):
                continue
            if piece.color == SideColor.WHITE:
                self.white_pieces.add(piece)
            else:
                self.black_pieces.add(piece)

    def print_grid(self) -> None:
        """TODO
        """
        print(" " + "   ".join(COLUMNS))
        for piece, _ in GridIter(self, on_new_row=lambda r : print(ROWS[r])):
            print(f" {Piece.get_str(piece)} ", end="")

    def get_str_grid(self) -> list[list[str]]:
        """TODO
        """
        str_grid: list[list[str]] = [[]]
        for piece, coord in GridIter(self, on_new_row=lambda _: str_grid.append([])):
            str_grid[coord.row].append(Piece.get_str(piece))

        return str_grid

    @staticmethod
    def get_start_grid() -> Grid:
        """TODO
        """
        return Grid.from_str_grid(BOARD_START)

    @staticmethod
    def from_str_grid(str_grid: list[list[str]]) -> Grid:
        """TODO
        """
        if len(str_grid) != len(ROWS):
            raise InvalidGridError("Invalid row count")

        grid: list[list[OptPiece]] = []
        for r, row in enumerate(str_grid):
            if len(row) != len(COLUMNS):
                raise InvalidGridError("Invalid column count")

            grid.append([])
            for c, piece_str in enumerate(row):
                grid[r].append(Piece.parse_from_str(piece_str, Coord(r, c)))

        return Grid(grid)


    def get_serialization_attrs(self) -> dict[str, Any]:
        return {
            "grid": self.get_start_grid()
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
    coord_ptr: Coord = Coord(0, 0)
    # Called on new row, with the current row value
    on_new_row: Callable[[int], None] = lambda _: None

    def __post_init__(self) -> None:
        #Check if initial coord_ptr raises GridInvalidCoordError
        self.grid.get_at(self.coord_ptr)

    def __iter__(self) -> GridIter:
        return self

    def __next__(self) -> tuple[OptPiece, Coord]:
        if self.coord_ptr.row >= L_ROWS:
            raise StopIteration
        if self.coord_ptr.column >= L_COLUMNS:
            self.on_new_row(self.coord_ptr.row)
            self.coord_ptr = Coord(self.coord_ptr.row+1, 0)
            return next(self)

        result = (self.grid.get_at(self.coord_ptr), self.coord_ptr)
        self.coord_ptr = Coord(self.coord_ptr.row, self.coord_ptr.column+1)
        return result
