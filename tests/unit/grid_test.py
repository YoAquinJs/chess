"""TODO"""
# pylint: disable=undefined-variable unused-variable

import random
from copy import deepcopy
from typing import Callable, Iterable

import pytest
from hypothesis import given
from hypothesis import strategies as st

from chess_engine.enums import PieceType, SideColor
from chess_engine.grid import BOARD_START, L_COLUMNS, L_ROWS, Grid, GridIter
from chess_engine.piece import NULL_PIECE_STR, Piece
from chess_engine.structs import Coord
from utils.exceptions import GridInvalidCoordError, InvalidGridError


@st.composite
def matrix_grids[T](draw: st.DrawFn, piece_st: st.SearchStrategy[T],
                    rows: int=L_ROWS, cols: int=L_COLUMNS) -> list[list[T]]:
    """TODO
    """
    matrix: list[list[T]] = []
    for r in range(rows):
        matrix.append([])
        for c in range(cols):
            piece = draw(piece_st)
            if isinstance(piece, Piece):
                piece.coord = Coord(r, c)
            matrix[r].append(piece)

    return matrix

@st.composite
def out_of_bounds_matrix_grids[T](draw: st.DrawFn, piece_st: st.SearchStrategy[T]
                           ) -> list[list[T]]:
    """TODO
    """
    rows = draw(st.integers(min_value=0, max_value=16))
    cols = draw(st.integers(min_value=0, max_value=16).filter(
        lambda x: x != L_COLUMNS if rows == L_ROWS else True))

    grid_st: st.SearchStrategy[list[list[T]]] = matrix_grids(piece_st, rows, cols)
    grid:list[list[T]] = draw(grid_st)
    return grid

def grids(piece_st: st.SearchStrategy[str]) -> st.SearchStrategy[Grid]:
    """TODO
    """
    return st.builds(Grid.from_str_grid, matrix_grids(piece_st))

def coords(min_val: int=0, max_val: int=L_ROWS-1) -> st.SearchStrategy[Coord]:
    """TODO
    """
    return st.builds(Coord,
              row=st.integers(min_value=min_val, max_value=max_val),
              column=st.integers(min_value=min_val, max_value=max_val)
              )
out_of_bounds_coords = st.one_of(coords(-11, -1), coords(8, 18))

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

def gen_random_coord_grid(pieces_set: Iterable[Piece | None], seed: int=42) -> Grid:
    """TODO
    """
    random.seed(seed)

    none_grid = Grid([[None for _ in range(L_COLUMNS)] for _ in range(L_ROWS)])
    for piece in pieces_set:
        coord = Coord(random.randint(0, 7), random.randint(0, 7))
        while none_grid.get_at(coord) is not None:
            coord = Coord(random.randint(0, 7), random.randint(0, 7))
        none_grid.set_at(coord, piece)

    return none_grid

def assert_grid_inmutability(grid: Grid, prev_grid: Grid, *exceptions: Coord) -> bool:
    """TODO
    """
    for piece, coord in GridIter(grid):
        if coord in exceptions:
            continue
        if piece != prev_grid.get_at(coord):
            return False

    return True


def test_start_grid_init() -> None:
    """Tests start grid generation, and assert it's value"""
    assert Grid.get_start_grid() == Grid.from_str_grid(BOARD_START)

@given(matrix_grids(optional_pieces))
def test_grid_piece_init(grid: list[list[Piece | None]]) -> None:
    """Tests grid generation of piece grid, for valid grids"""
    try:
        Grid(grid)
    except InvalidGridError:
        pytest.fail("Valid grid recognized as invalid")

@given(matrix_grids(optional_str_pieces))
def test_grid_str_init(grid: list[list[str]]) -> None:
    """Tests grid generation of string grid, for valid grids"""
    try:
        Grid.from_str_grid(grid)
    except InvalidGridError:
        pytest.fail("Valid grid recognized as invalid")

@given(out_of_bounds_matrix_grids(optional_pieces))
def test_grid_piece_init_out_of_bounds(grid: list[list[Piece | None]]) -> None:
    """TODO
    """
    with pytest.raises(InvalidGridError):
        Grid(grid)

@given(out_of_bounds_matrix_grids(optional_str_pieces))
def test_grid_str_init_out_of_bounds(grid: list[list[str]]) -> None:
    """TODO
    """
    with pytest.raises(InvalidGridError):
        Grid.from_str_grid(grid)

@given(matrix_grids(optional_pieces), st.lists(pieces(coords()), min_size=8, max_size=16))
def test_grid_equality(grid: list[list[Piece | None]], given_pieces: list[Piece | None]) -> None:
    """TODO
    """
    assert gen_random_coord_grid(given_pieces, 1) != gen_random_coord_grid(given_pieces, 2)

    generated_grid = Grid(grid)
    assert generated_grid == Grid(grid)
    assert generated_grid != [[None]]

@given(matrix_grids(optional_pieces), coords())
def test_grid_get(grid: list[list[Piece | None]], given_coord: Coord) -> None:
    """TODO
    """
    generated_grid = Grid(grid)
    assert grid[given_coord.row][given_coord.column] == generated_grid.get_at(given_coord)
    assert assert_grid_inmutability(generated_grid, Grid(grid))

@given(grids(optional_str_pieces), st.tuples(coords(), optional_pieces))
def test_grid_set(grid: Grid, coord_piece: tuple[Coord, Piece | None]) -> None:
    """TODO
    """
    prev_grid = deepcopy(grid)
    coord, piece = coord_piece

    prev_piece = grid.set_at(coord, piece)
    assert prev_piece == prev_grid.get_at(coord)
    assert grid.get_at(coord) == piece
    assert assert_grid_inmutability(grid, prev_grid, coord)

@given(grids(optional_str_pieces), coords(), coords())
def test_grid_swap(grid: Grid, coord1: Coord, coord2: Coord) -> None:
    """TODO
    """

    prev_grid = deepcopy(grid)
    if coord1 == coord2:
        with pytest.raises(GridInvalidCoordError):
            grid.swap_pieces(coord1, coord2)
        return

    grid.swap_pieces(coord1, coord2)

    swaped1 = grid.get_at(coord2)
    swaped2 = grid.get_at(coord1)
    prev1 = prev_grid.get_at(coord1)
    prev2 = prev_grid.get_at(coord2)

    assert prev1 is None if swaped1 is None else \
        swaped1.coord == coord2 and swaped1.same_piece_as(prev1)
    assert prev2 is None if swaped2 is None else \
        swaped2.coord == coord1 and swaped2.same_piece_as(prev2)
    assert assert_grid_inmutability(grid, prev_grid, coord1, coord2)

@given(grids(optional_str_pieces), out_of_bounds_coords, out_of_bounds_coords)
def test_grid_opt_bounds(grid: Grid, coord1: Coord, coord2: Coord) -> None:
    """TODO
    """
    with pytest.raises(GridInvalidCoordError):
        grid.get_at(coord1)

    with pytest.raises(GridInvalidCoordError):
        grid.set_at(coord1, None)

    with pytest.raises(GridInvalidCoordError):
        grid.swap_pieces(coord1, coord2)

@given(st.sets(pieces(coords()), min_size=8, max_size=16))
def test_grid_piece_sets(given_pieces: set[Piece]) -> None:
    """TODO
    """
    grid = gen_random_coord_grid(given_pieces)

    assert grid.white_pieces == {p for p in given_pieces if p.color == SideColor.WHITE}
    assert grid.black_pieces == {p for p in given_pieces if p.color == SideColor.BLACK}

@given(matrix_grids(optional_str_pieces))
def test_grid_get_str_grid(grid: list[list[str]]) -> None:
    """TODO
    """
    generated_grid = Grid.from_str_grid(grid)
    for r, row in enumerate(grid):
        for c, piece in enumerate(row):
            assert piece == Piece.get_str(generated_grid.get_at(Coord(r, c)))

# @given(grids(optional_str_pieces))
# def test_grid_iter(grid: Grid, coord1: Coord, coord2: Coord) -> None:
#     """TODO
#     """
#     with pytest.raises(GridInvalidCoordError):
#         grid.get_at(coord1)

#     with pytest.raises(GridInvalidCoordError):
#         grid.set_at(coord1, None)

#     with pytest.raises(GridInvalidCoordError):
#         grid.swap_pieces(coord1, coord2)
