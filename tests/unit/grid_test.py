"""TODO"""
# pylint: disable=undefined-variable unused-variable

import random
# from copy import copy
from typing import Callable

import pytest
from hypothesis import given
from hypothesis import strategies as st

from chess_engine.enums import PieceType, SideColor
from chess_engine.grid import BOARD_START, COLUMNS, ROWS, Grid  # , GridIter
from chess_engine.piece import NULL_PIECE_STR, Piece
from chess_engine.structs import Coord
from utils.exceptions import InvalidGridError


def grids[T](piece_st: st.SearchStrategy[T], rows: int=len(ROWS), cols: int=len(COLUMNS)
             ) -> st.SearchStrategy[list[list[T]]]:
    """TODO
    """
    return st.lists(st.lists(piece_st, min_size=cols, max_size=cols), min_size=rows, max_size=rows)

@st.composite
def out_of_bounds_grids[T](draw: st.DrawFn, piece_st: st.SearchStrategy[T]
                           ) -> list[list[T]]:
    """TODO
    """
    rows = draw(st.integers(min_value=7, max_value=9))
    cols = draw(st.integers(min_value=0, max_value=10).filter(\
        lambda x: x != len(COLUMNS) if rows == len(ROWS) else True))
    grid = draw(grids(piece_st, rows, cols))
    return grid

def coords(min_val: int=0, max_val: int=len(ROWS)-1) -> st.SearchStrategy[Coord]:
    """TODO
    """
    return st.builds(Coord,
              row=st.integers(min_value=min_val, max_value=max_val),
              column=st.integers(min_value=min_val, max_value=max_val)
              )

def pieces(coords_st: st.SearchStrategy[Coord]) -> st.SearchStrategy[Piece]:
    """TODO
    """
    return st.builds(Piece,
              type=st.sampled_from(PieceType),
              color=st.sampled_from(SideColor),
              coord=coords_st
              )
optional_pieces = st.none() | pieces(coords())
piece_str_build: Callable[[SideColor, PieceType], str] = lambda col,typ: col.value+typ.value
str_pieces = st.builds(piece_str_build,
                       st.sampled_from(SideColor),
                       st.sampled_from(PieceType)
                       )
optional_str_pieces = st.just(NULL_PIECE_STR) | str_pieces


def test_start_grid_generation() -> None:
    """Tests start grid generation, and assert it's value"""
    assert Grid.get_start_grid() == Grid.from_str_grid(BOARD_START)

@given(grids(optional_pieces))
def test_grid_piece_generation(grid: list[list[Piece | None]]) -> None:
    """Tests grid generation of piece grid, for valid grids"""
    try:
        Grid(grid)
    except InvalidGridError:
        pytest.fail("Grid recognized valid grid as invalid")

@given(grids(optional_str_pieces))
def test_grid_str_generation(grid: list[list[str]]) -> None:
    """Tests grid generation of string grid, for valid grids"""
    try:
        Grid.from_str_grid(grid)
    except InvalidGridError:
        pytest.fail("Grid recognized valid grid as invalid")

@given(out_of_bounds_grids(optional_pieces))
def test_grid_piece_generation_out_of_bounds(grid: list[list[Piece | None]]) -> None:
    """TODO
    """
    with pytest.raises(InvalidGridError):
        Grid(grid)

@given(out_of_bounds_grids(optional_str_pieces))
def test_grid_str_generation_out_of_bounds(grid: list[list[str]]) -> None:
    """TODO
    """
    with pytest.raises(InvalidGridError):
        Grid.from_str_grid(grid)

@given(grids(optional_pieces), st.sets(optional_pieces, min_size=8, max_size=16))
def test_grid_equality(grid: list[list[Piece | None]], pieces_set: set[Piece | None]) -> None:
    """TODO
    """

    def gen_random_coord_grid(pieces_set: set[Piece | None], seed: int) -> Grid:
        random.seed(seed)
        none_grid = Grid([[None for _ in range(len(COLUMNS))] for _ in range(len(ROWS))])
        for piece in pieces_set:
            coord = Coord(random.randint(0, 7), random.randint(0, 7))
            while none_grid.get_at(coord) is not None:
                coord = Coord(random.randint(0, 7), random.randint(0, 7))
            none_grid.set_at(coord, piece)
        return none_grid
    assert gen_random_coord_grid(pieces_set, 1) != gen_random_coord_grid(pieces_set, 2)

    generated_grid = Grid(grid)
    assert generated_grid == Grid(grid)
    assert generated_grid != [[None]]


# @pytest.mark.parametrize("grid, valid", [
#     (Coord(0,0),   True),
#     (Coord(7,7),   True),
#     (Coord(-1,0),  False),
#     (Coord(8,0),   False),
#     (Coord(0,-1),  False),
#     (Coord(0,8),   False),
#     (Coord(-1,-1), False),
#     (Coord(8,8),   False),
# ])
# def test_grid_get_boundaries(coord: Coord, valid: bool) -> None:
#     """TODO
#     """
#     grid = Grid.get_start_grid()
#     _valid = True
#     try:
#         grid.get_at(coord)
#     except IndexError:
#         _valid = False
#     finally:
#         assert _valid == valid

# @pytest.mark.parametrize("coord, expected", [
#     (Coord(0,0), Piece(PieceType.ROOK, SideColor.BLACK, Coord(0,0))),
#     (Coord(1,0), Piece(PieceType.PAWN, SideColor.BLACK, Coord(1,0))),
#     (Coord(2,0), None),
#     (Coord(5,4), None),
#     (Coord(4,7), None),
#     (Coord(7,4), Piece(PieceType.KING, SideColor.WHITE, Coord(7,4))),
#     (Coord(6,4), Piece(PieceType.PAWN, SideColor.WHITE, Coord(6,4))),
#     (Coord(7,7), Piece(PieceType.ROOK, SideColor.WHITE, Coord(7,7))),
# ])
# def test_grid_get(coord: Coord, expected: Optional[Piece]) -> None:
#     """TODO
#     """
#     grid = Grid.get_start_grid()
#     assert grid.get_at(coord) == expected

# @pytest.mark.parametrize("coord, piece", [
#     (Coord(0,0), Piece(PieceType.ROOK, SideColor.BLACK, Coord(0,0))),
#     (Coord(1,0), Piece(PieceType.PAWN, SideColor.BLACK, Coord(1,0))),
#     (Coord(2,0), None),
#     (Coord(5,4), None),
#     (Coord(4,7), None),
#     (Coord(7,4), Piece(PieceType.KING, SideColor.WHITE, Coord(7,4))),
#     (Coord(6,4), Piece(PieceType.PAWN, SideColor.WHITE, Coord(6,4))),
#     (Coord(7,7), Piece(PieceType.ROOK, SideColor.WHITE, Coord(7,7))),
# ])
# def test_grid_set(coord: Coord, piece: Optional[Piece]) -> None:
#     """TODO
#     """
#     empty_grid = [
#         ['','','','','','','',''],
#         ['','','','','','','',''],
#         ['','','','','','','',''],
#         ['','','','','','','',''],
#         ['','','','','','','',''],
#         ['','','','','','','',''],
#         ['','','','','','','',''],
#         ['','','','','','','',''],
#     ]
#     grid = Grid.from_str_grid(empty_grid)
#     grid.set_at(coord, piece)
#     assert grid.get_at(coord) == piece

# @pytest.mark.parametrize("coord1, coord2", [
#     (Coord(0,0), Coord(4,3)),
#     (Coord(1,0), Coord(1,6)),
#     (Coord(2,0), Coord(2,2)),
#     (Coord(5,4), Coord(4,4)),
#     (Coord(4,7), Coord(2,7)),
#     (Coord(7,4), Coord(0,4)),
#     (Coord(6,4), Coord(4,6)),
#     (Coord(7,7), Coord(0,0)),
# ])
# def test_grid_swap(coord1: Coord, coord2: Coord) -> None:
#     """TODO
#     """
#     grid = Grid.get_start_grid()
#     piece1 = copy(grid.get_at(coord1))
#     piece2 = copy(grid.get_at(coord2))
#     grid.swap_pieces(coord1, coord2)
#     assert grid.get_at(coord1) == piece2 and grid.get_at(coord2) == piece1

# @pytest.mark.parametrize("start", [
#     (Coord(0,0)),
#     (Coord(1,0)),
#     (Coord(2,0)),
#     (Coord(5,4)),
#     (Coord(4,7)),
#     (Coord(7,4)),
#     (Coord(6,4)),
#     (Coord(7,7)),
# ])
# def test_grid_iterator(start: Coord) -> None:
#     """TODO
#     """
#     grid = Grid.get_start_grid()
#     pieces: list[Optional[Piece]] = []
#     for r in range(start.row, len(ROWS)):
#         for c in range(start.column, len(COLUMNS)):
#             pieces.append(Piece.parse_from_str(BOARD_START[r][c], Coord(r,c)))
#     iter_pieces = list(GridIter(grid))
#     assert iter_pieces == pieces

# def test_grid_serialization(grid: Grid) -> None:
#     """TODO
#     """
#     pass
