"""TODO"""
# pylint: disable=undefined-variable

from typing import Callable

from hypothesis import strategies as st

from chess_engine.enums import PieceType, SideColor
from chess_engine.grid import L_COLUMNS, L_ROWS, Grid
from chess_engine.piece import NULL_PIECE_STR, Piece
from chess_engine.structs import Coord

# Struct Strategies

def coords(min_val: int=0, max_val: int=L_ROWS-1) -> st.SearchStrategy[Coord]:
    """TODO
    """
    return st.builds(Coord,
              row=st.integers(min_value=min_val, max_value=max_val),
              column=st.integers(min_value=min_val, max_value=max_val)
              )
out_of_bounds_coords = st.one_of(coords(-11, -1), coords(8, 18))

# Piece Strategies

def pieces(coords_st: st.SearchStrategy[Coord]) -> st.SearchStrategy[Piece]:
    """TODO
    """
    return st.builds(Piece,
              type=st.sampled_from(PieceType),
              color=st.sampled_from(SideColor),
              coord=coords_st
              )
opt_pieces = st.none() | pieces(coords())

piece_str_build: Callable[[SideColor, PieceType], str] = lambda col,typ: col.value+typ.value
str_pieces = st.builds(piece_str_build,
                       st.sampled_from(SideColor),
                       st.sampled_from(PieceType)
                       )
opt_str_pieces = st.just(NULL_PIECE_STR) | str_pieces

# Grid Strategies

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

def grids(optional: bool=True) -> st.SearchStrategy[Grid]:
    """TODO
    """
    return st.builds(Grid.from_str_grid, matrix_grids(opt_str_pieces if optional else str_pieces))
