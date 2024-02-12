"""TODO"""

from typing import Optional

import pytest

from chess_engine.enums import PieceType, SideColor
from chess_engine.grid import BOARD_START, Grid
from chess_engine.piece import Piece
from chess_engine.structs import Coord
from utils.exceptions import InvalidGridError


def test_grid_initialization() -> None:
    """TODO
    """
    pawn = Piece(PieceType.PAWN, SideColor.WHITE, Coord(0,0))
    list_grid = [
        [pawn,None,None,None,None,None,None,pawn],
        [None,pawn,None,None,None,None,pawn,None],
        [None,None,pawn,None,None,pawn,pawn,pawn],
        [None,None,None,pawn,pawn,None,None,None],
        [None,None,None,pawn,pawn,None,None,None],
        [None,None,pawn,None,None,pawn,None,None],
        [None,pawn,None,None,None,None,pawn,pawn],
        [pawn,None,None,None,None,None,None,pawn],
    ]
    str_list_grid = [
        ['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', '  ', '  '],
        ['bP', '  ', '  ', 'bP', 'bP', 'bP', 'bP', 'bP'],
        ['  ', 'bP', '  ', '  ', '  ', 'bK', '  ', '  '],
        ['wR', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
        ['  ', 'wP', 'bP', '  ', 'w@', '  ', '  ', '  '],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', 'bR'],
        ['wP', '  ', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
        ['  ', 'wK', 'wB', 'wQ', '  ', 'wB', 'wK', 'wR']
    ]
    Grid(list_grid)
    Grid.from_str_grid(str_list_grid)
    Grid.get_start_grid()

@pytest.mark.parametrize("grid, valid", [
    (BOARD_START,
     True),
    ([['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', '  '],
      ['bP', '  ', '  ', 'bP', 'bP', 'bP', 'bP', 'bP'],
      ['  ', 'bP', '  ', '  ', '  ', 'bK', '  ', '  '],
      ['wR', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['  ', 'wP', 'bP', '  ', 'w@', '  ', '  ', '  '],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', 'bR'],
      ['wP', '  ', 'wP', 'wP', 'wP', 'wP', 'wP'],
      ['  ', 'wK', 'wB', 'wQ', '  ', 'wB', 'wK', 'wR']],
      False),
    ([['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR', '  '],
      ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
      ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR']],
      False),
    ([['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
      ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR'],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR'],
      ['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR'],
      ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP']],
      False),
    ([['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR'],
      ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
      ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR']],
      False),
])
def test_grid_boundaries(grid: list[list[str]], valid: bool) -> None:
    """TODO
    """
    _valid = True
    try:
        Grid.from_str_grid(grid)
    except InvalidGridError:
        _valid = False
    finally:
        assert _valid == valid

@pytest.mark.parametrize("grid, valid", [
    (Coord(0,0), True),
    (Coord(7,7), True),
    (Coord(-1,0), False),
    (Coord(8,0), False),
    (Coord(0,-1), False),
    (Coord(0,8), False),
    (Coord(-1,-1), False),
    (Coord(8,8), False),
])
def test_grid_get_boundaries(coord: Coord, valid: bool) -> None:
    """TODO
    """
    grid = Grid.get_start_grid()
    _valid = True
    try:
        grid.get_at(coord)
    except IndexError:
        _valid = False
    finally:
        assert _valid == valid

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

@pytest.mark.parametrize("grid1, grid2, equal", [
    (BOARD_START,
     BOARD_START,
     True),
    ([['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', '  ', '  '],
      ['bP', '  ', '  ', 'bP', 'bP', 'bP', 'bP', 'bP'],
      ['  ', 'bP', '  ', '  ', '  ', 'bK', '  ', '  '],
      ['wR', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['  ', 'wP', 'bP', '  ', 'w@', '  ', '  ', '  '],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', 'bR'],
      ['wP', '  ', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
      ['  ', 'wK', 'wB', 'wQ', '  ', 'wB', 'wK', 'wR']],
     [['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', '  ', '  '],
      ['bP', '  ', '  ', 'bP', 'bP', 'bP', 'bP', 'bP'],
      ['  ', 'bP', '  ', '  ', '  ', 'bK', '  ', '  '],
      ['wR', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['  ', 'wP', 'bP', '  ', 'w@', '  ', '  ', '  '],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', 'bR'],
      ['wP', '  ', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
      ['  ', 'wK', 'wB', 'wQ', '  ', 'wB', 'wK', 'wR']],
     True),
    ([['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
      ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR'],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR'],
      ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP']],
     [['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
      ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR'],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR'],
      ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP']],
     True),
    ([['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR'],
      ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
      ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR']],
     [['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR'],
      ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
      ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR']],
     False),
    ([['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR'],
      ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
      ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR']],
     [['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR'],
      ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR']],
     False),
    ([['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR'],
      ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
      ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR']],
     [['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR'],
      ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
      ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
      ['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR']],
     False),
])
def test_grid_equality(grid1: list[list[str]], grid2: list[list[str]], equal: bool) -> None:
    """TODO
    """
    assert (Grid.from_str_grid(grid1) == Grid.from_str_grid(grid2)) == equal

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
