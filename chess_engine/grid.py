"""This module contains the grid class for handling the boards piece grid"""

from __future__ import annotations

from typing import Optional

from chess_engine.piece import Piece
from chess_engine.structs import Coord
from game_logic.consts import COLUMNS, ROWS


class Grid():
    """TODO
    """

    def __init__(self, grid: list[list[Optional[Piece]]]) -> None:
        self.__grid = grid

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
        prev_piece = self.__grid[coord.row][coord.column]
        self.__grid[coord.row][coord.column] = piece
        return prev_piece

    def swap_pieces(self, coord1: Coord, coord2: Coord) -> None:
        """Swaps the pieces in the given coordinates

        Args:
            coord1 (Coord): Coordinate 1
            coord2 (Coord): Coordinate 2
        """
        piece1 = self.get_at(coord1)
        if piece1 is not None:
            piece1.row = coord2.row
            piece1.column = coord2.column
        piece2 = self.get_at(coord1)
        if piece2 is not None:
            piece2.row = coord1.row
            piece2.column = coord1.column

        self.set_at(coord1, piece2)
        self.set_at(coord2, piece1)

    def print_grid(self) -> None:
        """TODO
        """
        for ri, r in enumerate(['',ROWS]):
            print(r, end='')
            for ci, c in enumerate(COLUMNS):
                if ri == 0:
                    print(c, end='')
                piece = self.get_at(Coord(ri-1, ci))
                print(f"{'##' if piece is None else str(piece)} ", end='')

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