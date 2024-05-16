"""TODO"""

from hypothesis import given

from chess_engine.enums import PieceType, SideColor
from chess_engine.grid import L_ROWS
from chess_engine.piece import Piece
from chess_engine.structs import Coord
from utils.test_strategies import coords, opt_str_pieces, pieces


@given(pieces(coords()))
def test_piece_equality(given_piece: Piece) -> None:
    """TODO
    """
    assert given_piece != (given_piece.type, given_piece.color, given_piece.coord)
    assert given_piece == Piece(given_piece.type, given_piece.color, given_piece.coord)

    column = given_piece.coord.column
    diff_coord = Coord(given_piece.coord.row, column+1 if column+1 < L_ROWS else 0)
    assert given_piece != Piece(given_piece.type, given_piece.color, diff_coord)
    assert given_piece.same_as(Piece(given_piece.type, given_piece.color, diff_coord))

@given(opt_str_pieces)
def test_piece_str_funcs(given_piece: str) -> None:
    """TODO
    """
    piece = Piece.from_str(given_piece, Coord(0,0))
    assert given_piece == Piece.get_str(piece)

@given(pieces(coords()))
def test_piece_hashing(given_piece: Piece) -> None:
    """TODO
    """
    assert hash(given_piece) == hash(Piece(given_piece.type, given_piece.color, given_piece.coord))

    diff_type = [t for t in PieceType if t is not given_piece.type][0]
    diff_color = SideColor.WHITE if given_piece.color is SideColor.BLACK else SideColor.BLACK
    column = given_piece.coord.column
    diff_coord = Coord(given_piece.coord.row, column+1 if column+1 < L_ROWS else 0)

    assert hash(given_piece) != hash(Piece(diff_type, given_piece.color, given_piece.coord))
    assert hash(given_piece) != hash(Piece(given_piece.type, diff_color, given_piece.coord))
    assert hash(given_piece) != hash(Piece(given_piece.type, given_piece.color, diff_coord))
