"""This module contains the Board model object and it's properties"""

from __future__ import annotations

from copy import deepcopy
from typing import Optional

from chess_engine.chess_game_data import Movement
from chess_engine.enums import MoveStatus, TurnState, ValidationStatus
from chess_engine.grid import COLUMNS, ROWS, Grid
from chess_engine.piece import MovSpecialCase, Piece, PieceType, SideColor
from chess_engine.structs import CastlingState, Coord, Dir
from utils.exceptions import StaticClassInstanceError

GridContext = tuple[SideColor, Grid]
ValidationResult = tuple[Optional[MoveStatus], Optional[CastlingState]]
class ChessValidator:
    """TODO
    """

    initial_piece_count = {
        PieceType.PAWN : 8,
        PieceType.BISHOP : 2,
        PieceType.KNIGTH : 2,
        PieceType.ROOK : 2,
        PieceType.QUEEN : 1,
        PieceType.KING : 1
    }
    white_initial_row = 1
    white_pawn_initial_row = 2
    black_initial_row = 8
    black_pawn_initial_row = 7

    _cached_grid_ctx: GridContext
    _cached_movements: dict[tuple[Coord, Coord], ValidationStatus] = {}

    @classmethod
    def clean_cache(cls, new_grid_ctx: GridContext) -> None:
        """TODO
        """
        cls._cached_grid_ctx = new_grid_ctx
        cls._cached_movements = {}

    @classmethod
    def _access_cache(cls, mov: tuple[Coord, Coord],
                      grid_ctx: GridContext) -> Optional[ValidationStatus]:
        if cls._cached_grid_ctx == grid_ctx:
            return cls._cached_movements[mov]
        return None

    @classmethod
    def is_valid_initial_grid(cls) -> bool:
        """TODO
        """
        grid = Grid.get_start_grid()

        white_pieces = {piece_type: 0 for piece_type in PieceType}
        for piece in grid.white_pieces:
            white_pieces[piece.type] += 1
            if piece.type == PieceType.PAWN and piece.coord.column != cls.white_pawn_initial_row:
                return False
            if piece.type != PieceType.PAWN and piece.coord.column != cls.white_initial_row:
                return False
        black_pieces = {piece_type: 0 for piece_type in PieceType}
        for piece in grid.black_pieces:
            black_pieces[piece.type] += 1
            if piece.type == PieceType.PAWN and piece.coord.column != cls.black_pawn_initial_row:
                return False
            if piece.type != PieceType.PAWN and piece.coord.column != cls.black_initial_row:
                return False

        for piece_type, ideal_count in cls.initial_piece_count.items():
            if white_pieces[piece_type] != ideal_count or black_pieces[piece_type] != ideal_count:
                return False
        return True

    @classmethod
    def is_valid_promotion_type(cls, piece_type: PieceType) -> bool:
        """TODO
        """
        return piece_type not in (PieceType.PAWN, PieceType.KING)

    @classmethod
    def is_valid_move(cls, origin: Coord, dest: Coord,
                      context: tuple[Optional[Movement], TurnState, CastlingState, GridContext]
                      ) -> ValidationResult:
        """TODO
        """
        last_mov, turn_state, castling_state, grid_ctx = context
        validation = cls._access_cache((origin, dest), grid_ctx)
        if validation is None:
            validation = cls._is_valid_move(origin, dest, grid_ctx)
        match validation:
            case ValidationStatus.INVALID:
                return MoveStatus.INVALID, None
            case ValidationStatus.CHECKS_KING:
                return MoveStatus.INVALID, None
            case ValidationStatus.NEED_LAST_MOVE:
                ctx = (last_mov, grid_ctx)
                is_valid = cls._is_valid_enpassant(origin, dest, ctx)
                return None if is_valid else MoveStatus.INVALID, None
            case ValidationStatus.NEED_CASTLING_STATE:
                ctx = (turn_state, castling_state, grid_ctx)
                is_valid, new_castling = cls._is_valid_castle(origin, dest, ctx)
                return None if is_valid else MoveStatus.INVALID, new_castling
            case ValidationStatus.NEED_PROMOTION_PIECE:
                return MoveStatus.REQUIRE_PROMOTION, None
            case _:
                return None, None

    @classmethod
    def _is_valid_move(cls, origin: Coord, dest: Coord, grid_ctx: GridContext) -> ValidationStatus:
        turn, grid = grid_ctx

        if origin == dest:
            return ValidationStatus.INVALID

        o_piece = grid.get_at(origin)
        if o_piece is None or o_piece.color != turn:
            return ValidationStatus.INVALID

        direction = origin.get_dir_to(dest)
        if o_piece.extendable_mov:
            direction = direction.normalized()

        d_piece = grid.get_at(dest)
        if d_piece is not None and d_piece.color == o_piece.color:
            return ValidationStatus.INVALID

        mov_case = o_piece.movements.get(direction, None)
        if mov_case is None:
            return ValidationStatus.INVALID

        if mov_case is MovSpecialCase.CASTLE:
            return ValidationStatus.NEED_CASTLING_STATE

        #pawn special cases
        if mov_case is MovSpecialCase.DOUBLE_PAWN_MOVE:
            if not cls._has_clear_path(origin, dest, direction, grid) or d_piece is not None:
                return ValidationStatus.INVALID
        elif mov_case is MovSpecialCase.PAWN_ATTACK and d_piece is None: #possible en passant move
            return ValidationStatus.NEED_LAST_MOVE
        elif mov_case is MovSpecialCase.PAWN_MOVE and d_piece is not None:
            return ValidationStatus.INVALID

        if o_piece.extendable_mov and not cls._has_clear_path(origin, dest, direction, grid):
            return ValidationStatus.INVALID

        #movement does not leaves player in check
        grid_copy = deepcopy(grid)
        if d_piece is not None:
            grid_copy.set_at(dest, None)
        grid_copy.swap_pieces(origin, dest)
        pieces = grid.white_pieces if turn == SideColor.WHITE else grid.black_pieces
        opponent_pieces = grid.white_pieces if turn == SideColor.BLACK else grid.black_pieces
        king = [p for p in pieces if p.type == PieceType.KING][0]
        is_in_check = any(cls._attacks_coord(p, king, (turn, grid_copy)) for p in opponent_pieces)
        if is_in_check:
            return ValidationStatus.INVALID

        # From here the move is valid
        if d_piece is not None and d_piece.type == PieceType.KING:
            return ValidationStatus.CHECKS_KING

        if cls._is_promotion(o_piece, dest):
            return ValidationStatus.NEED_PROMOTION_PIECE

        return ValidationStatus.VALID

    @classmethod
    def _is_promotion(cls, piece: Piece, dest: Coord) -> bool:
        p_row = cls.black_initial_row if piece.color == SideColor.WHITE else cls.white_initial_row
        return piece.type == PieceType.PAWN and p_row == dest.row

    @classmethod
    def _has_clear_path(cls, origin: Coord, dest: Coord, direction: Dir, grid: Grid) -> bool:
        _coord = origin
        _dest = dest.dir(direction, -1)
        while _coord != _dest:
            if grid.get_at(_coord) is not None:
                return False
            _coord = _coord.dir(direction)

        return True

    @classmethod
    def _is_valid_enpassant(cls, origin: Coord, dest: Coord,
                           context: tuple[Optional[Movement],GridContext]) -> bool:
        raise NotImplementedError()

    @classmethod
    def _is_valid_castle(cls, origin: Coord, dest: Coord,
                         context: tuple[TurnState, CastlingState, GridContext]
                         ) -> tuple[bool, CastlingState]:
        raise NotImplementedError()

    @classmethod
    def get_board_state(cls, last_mov: Optional[Movement], castling_state: CastlingState,
                        grid_ctx: GridContext) -> TurnState:
        """TODO
        """
        turn, grid = grid_ctx

        pieces = grid.white_pieces if turn == SideColor.WHITE else grid.black_pieces
        opponent_pieces = grid.white_pieces if turn == SideColor.BLACK else grid.black_pieces
        king = [p for p in pieces if p.type == PieceType.KING][0]

        is_in_check = any(cls._attacks_coord(p, king, grid_ctx) for p in opponent_pieces)
        temp_state = TurnState.CHECK if is_in_check else TurnState.MOVE_TURN
        context = (last_mov, temp_state, castling_state, grid_ctx)
        any_valid_move = any(cls._any_valid_move(p, context) for p in pieces)

        if not any_valid_move:
            if is_in_check:
                return TurnState.CHECKMATE
            return TurnState.STALEMATE
        return temp_state

    @classmethod
    def _attacks_coord(cls, piece: Piece, attacked_p: Piece, grid_ctx: GridContext) -> bool:
        origin = piece.coord
        destination = attacked_p.coord
        validation = cls._is_valid_move(origin, destination, grid_ctx)
        return validation in (ValidationStatus.VALID, ValidationStatus.CHECKS_KING)

    @classmethod
    def _any_valid_move(cls, piece: Piece,
                        context: tuple[Optional[Movement], TurnState, CastlingState, GridContext]
                        ) -> bool:
        origin = piece.coord
        def extend_validation(direction: Dir) -> bool:
            i = 1
            dest = origin.dir(direction, i)
            while 0 < dest.row < len(ROWS) and 0 < dest.column < len(COLUMNS):
                validation, _ = cls.is_valid_move(origin, dest, context)
                if validation in (None, MoveStatus.REQUIRE_PROMOTION):
                    return True
                i += 1
                dest = origin.dir(direction, i)
            return False

        def non_extend_validation(direction: Dir) -> bool:
            dest = origin.dir(direction)
            validation, _ = cls.is_valid_move(origin, dest, context)
            return validation in (None, MoveStatus.REQUIRE_PROMOTION)

        validate_direction = extend_validation if piece.extendable_mov else non_extend_validation
        for possible_dir in piece.movements:
            if validate_direction(possible_dir):
                return True
        return False

    def __init__(self) -> None:
        raise StaticClassInstanceError(ChessValidator)
