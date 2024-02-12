"""TODO"""

from typing import Optional

import pytest

from chess_engine.enums import PieceType, SideColor
from chess_engine.grid import BOARD_START, Grid
from chess_engine.piece import Piece
from chess_engine.structs import Coord


def test_grid_initialization() -> None:
    """TODO
    """
    pass

def test_grid_boundaries() -> None:
    """TODO
    """
    pass

def test_grid_get(grid: Grid, coord: Coord, expected: Optional[Piece]) -> None:
    """TODO
    """
    pass

def test_grid_set(grid: Grid, coord: Coord, piece: Optional[Piece]) -> None:
    """TODO
    """
    pass

def test_grid_swap(grid: Grid, coord1: Coord, coord2: Coord) -> None:
    """TODO
    """
    pass

def test_grid_equality(grid1: list[list[str]], grid2: list[list[str]], expected: bool) -> None:
    """TODO
    """
    pass

def test_grid_iterator(grid: Grid) -> None:
    """TODO
    """
    pass

def test_grid_piece_lists(grid: Grid, expected: tuple[list[Piece], list[Piece]]) -> None:
    """TODO
    """
    pass

def test_grid_serialization(grid: Grid) -> None:
    """TODO
    """
    pass
