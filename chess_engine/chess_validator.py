"""This module contains the Board model object and it's properties"""

from __future__ import annotations

from copy import deepcopy
from typing import Optional, cast

from chess_engine.chess_game_data import Movement
from chess_engine.enums import MoveStatus, TurnState, ValidationStatus
from chess_engine.grid import COLUMNS, ROWS, Grid
from chess_engine.piece import MovSpecialCase, Piece, PieceType, SideColor
from chess_engine.structs import CastlingState, Coord, Dir
from utils.exceptions import StaticClassInstanceError
from utils.utils import opponent

GridContext = tuple[SideColor, Grid]
ValidationResult = tuple[Optional[MoveStatus], Optional[CastlingState], bool]
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
    def _save_to_cache(cls, mov: tuple[Coord, Coord], status: ValidationStatus) -> None:
        cls._cached_movements[mov] = status

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
            cls._save_to_cache((origin, dest), validation)

        validation_result: ValidationResult
        match validation:
            case ValidationStatus.VALID:
                new_castling = cls._get_castling_state(origin, grid_ctx[1], castling_state)
                validation_result =  (None, new_castling, False)
            case ValidationStatus.INVALID:
                validation_result = (MoveStatus.INVALID, None, False)
            case ValidationStatus.CHECKS_KING:
                validation_result = (MoveStatus.INVALID, None, False)
            case ValidationStatus.NEED_LAST_MOVE:
                if last_mov is None:
                    validation_result = (MoveStatus.INVALID, None, False)
                else:
                    ctx = (last_mov, grid_ctx)
                    is_valid = cls._is_valid_enpassant(origin, dest, ctx)
                    validation_result = (None if is_valid else MoveStatus.INVALID, None, False)
            case ValidationStatus.NEED_CASTLING_STATE:
                ctx = (turn_state, castling_state, grid_ctx)
                is_valid, new_castling = cls._is_valid_castle(origin, dest, ctx)
                state = None if is_valid else MoveStatus.INVALID
                validation_result = (state, new_castling, True)
            case ValidationStatus.NEED_PROMOTION_PIECE:
                validation_result = (MoveStatus.REQUIRE_PROMOTION, None, True)
        return validation_result

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
            if not cls._has_clear_path(origin, dest, grid) or d_piece is not None:
                return ValidationStatus.INVALID
        elif mov_case is MovSpecialCase.PAWN_ATTACK and d_piece is None: #possible en passant move
            return ValidationStatus.NEED_LAST_MOVE
        elif mov_case is MovSpecialCase.PAWN_MOVE and d_piece is not None:
            return ValidationStatus.INVALID

        if o_piece.extendable_mov and not cls._has_clear_path(origin, dest, grid):
            return ValidationStatus.INVALID

        if cls._is_left_in_check((origin, dest, d_piece, grid_ctx)):
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
    def _has_clear_path(cls, origin: Coord, dest: Coord, grid: Grid) -> bool:
        _coord = origin
        direction = origin.get_dir_to(dest).normalized()
        _dest = dest.dir(direction, -1)
        while _coord != _dest:
            if grid.get_at(_coord) is not None:
                return False
            _coord = _coord.dir(direction)

        return True

    @classmethod
    def _is_valid_enpassant(cls, origin: Coord, dest: Coord,
                            context: tuple[Movement, GridContext]) -> bool:
        last_mov, grid_ctx = context

        l_piece, l_dest = last_mov
        if l_piece.type != PieceType.PAWN or not isinstance(l_dest, Coord):
            return False
        l_piece_dir = l_piece.coord.get_dir_to(l_dest)
        if l_piece.movements[l_piece_dir] != MovSpecialCase.DOUBLE_PAWN_MOVE:
            return False
        l_mov_dir = l_piece_dir.normalized().row
        if l_dest.column != dest.column or l_dest.row-l_mov_dir != dest.row:
            return False

        if cls._is_left_in_check((origin, dest, None, grid_ctx)):
            return False
        return True

    @classmethod
    def _is_valid_castle(cls, origin: Coord, dest: Coord,
                         context: tuple[TurnState, CastlingState, GridContext]
                         ) -> tuple[bool, Optional[CastlingState]]:
        turn_state, castling_state, grid_ctx = context
        _, grid = grid_ctx
        if turn_state != TurnState.MOVE_TURN:
            return False, None

        king_column_in_path = origin.get_dir_to(dest).normalized().column
        is_left_dir = king_column_in_path < 0
        if (is_left_dir and not castling_state.left) or \
            (not is_left_dir and not castling_state.right):
            return False, None

        rook_coord = Coord(origin.row, 0 if is_left_dir else 7)
        rook__dest_coord = Coord(origin.row, 3 if is_left_dir else 5)
        if not cls._has_clear_path(rook_coord, rook__dest_coord, grid):
            return False, None
        if not cls._has_clear_path(origin, dest, grid):
            return False, None

        path_coord = Coord(origin.row, king_column_in_path)
        if cls._is_coord_attacked(path_coord, grid_ctx):
            return False, None

        if cls._is_left_in_check((origin, dest, None, grid_ctx)):
            return False, None

        return True, CastlingState(False, False)

    @classmethod
    def _is_left_in_check(cls, context: tuple[Coord, Coord, Optional[Piece], GridContext]) -> bool:
        origin, dest, d_piece, grid_ctx = context
        turn, grid = grid_ctx
        grid_copy = deepcopy(grid)
        if d_piece is not None:
            grid_copy.set_at(dest, None)
        grid_copy.swap_pieces(origin, dest)
        pieces = grid_copy.white_pieces if turn == SideColor.WHITE else grid_copy.black_pieces
        king = [p for p in pieces if p.type == PieceType.KING][0]
        return cls._is_coord_attacked(king.coord, (turn, grid_copy))

    @classmethod
    def _get_castling_state(cls, origin: Coord, grid: Grid,
                            castling_state: CastlingState) -> Optional[CastlingState]:
        piece = cast(Piece, grid.get_at(origin))
        if piece.type == PieceType.KING:
            return CastlingState(False, False)
        if piece.type == PieceType.ROOK:
            rook_pos = origin.get_dir_to(Coord(0, 4)).column
            if castling_state.left and rook_pos < 0:
                return CastlingState(False, castling_state.right)
            if castling_state.right and rook_pos > 0:
                return CastlingState(castling_state.left, False)
        return None

    @classmethod
    def get_board_state(cls, last_mov: Optional[Movement], castling_state: CastlingState,
                        grid_ctx: GridContext) -> TurnState:
        """TODO
        """
        turn, grid = grid_ctx

        pieces = grid.white_pieces if turn == SideColor.WHITE else grid.black_pieces
        king = [p for p in pieces if p.type == PieceType.KING][0]
        is_in_check = cls._is_coord_attacked(king.coord, grid_ctx)

        temp_state = TurnState.CHECK if is_in_check else TurnState.MOVE_TURN
        context = (last_mov, temp_state, castling_state, grid_ctx)
        any_valid_move = any(cls._any_valid_move(context, p) for p in pieces)

        if not any_valid_move:
            if is_in_check:
                return TurnState.CHECKMATE
            return TurnState.STALEMATE
        return temp_state

    @classmethod
    def _is_coord_attacked(cls, coord: Coord, grid_ctx: GridContext) -> bool:
        turn, grid = grid_ctx
        attacker = opponent(turn)
        attacker_pieces = grid.white_pieces if attacker == SideColor.WHITE else grid.black_pieces
        return any(cls._attacks_coord(p, coord, grid_ctx) for p in attacker_pieces)

    @classmethod
    def _attacks_coord(cls, piece: Piece, coord: Coord, grid_ctx: GridContext) -> bool:
        origin = piece.coord
        validation = cls._is_valid_move(origin, coord, grid_ctx)
        return validation in (ValidationStatus.VALID, ValidationStatus.CHECKS_KING)

    @classmethod
    def _any_valid_move(cls, context: tuple[Optional[Movement],TurnState,CastlingState,GridContext],
                        piece: Piece) -> bool:
        origin = piece.coord
        def extend_validation(direction: Dir) -> bool:
            i = 1
            dest = origin.dir(direction, i)
            while 0 < dest.row < len(ROWS) and 0 < dest.column < len(COLUMNS):
                validation, _, _ = cls.is_valid_move(origin, dest, context)
                if validation in (None, MoveStatus.REQUIRE_PROMOTION):
                    return True
                i += 1
                dest = origin.dir(direction, i)
            return False

        def non_extend_validation(direction: Dir) -> bool:
            dest = origin.dir(direction)
            validation, _, _ = cls.is_valid_move(origin, dest, context)
            return validation in (None, MoveStatus.REQUIRE_PROMOTION)

        validate_direction = extend_validation if piece.extendable_mov else non_extend_validation
        for possible_dir in piece.movements:
            if validate_direction(possible_dir):
                return True
        return False

    def __init__(self) -> None:
        raise StaticClassInstanceError(ChessValidator)
