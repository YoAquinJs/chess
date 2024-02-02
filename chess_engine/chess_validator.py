"""This module contains the Board model object and it's properties"""

from __future__ import annotations

from asyncio import run
from copy import deepcopy
from typing import Any, Optional, cast

from chess_engine.chess_game_data import Movement
from chess_engine.enums import MoveStatus, TurnState, ValidationStatus
from chess_engine.grid import COLUMNS, ROWS, Grid, GridIter
from chess_engine.piece import MovSpecialCase, Piece, PieceType, SideColor
from chess_engine.structs import CastlingState, Coord
from utils.exceptions import StaticClassInstanceError
from utils.utils import opponent

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
    def is_valid_move(cls, origin: Coord, dest: Coord, last_mov: Optional[Movement],
                      castling_state: CastlingState, grid_ctx: GridContext) -> ValidationResult:
        """TODO
        """
        validation = cls._access_cache((origin, dest), grid_ctx)
        if validation is None:
            validation = cls._is_valid_move(origin, dest, grid_ctx)
        match validation:
            case ValidationStatus.INVALID:
                return MoveStatus.INVALID, None
            case ValidationStatus.CHECKS_KING:
                return MoveStatus.INVALID, None
            case ValidationStatus.NEED_LAST_MOVE:
                context = (origin, dest, last_mov, grid_ctx)
                is_valid = cls._is_valid_enpassant(*context)
                return None if is_valid else MoveStatus.INVALID, None
            case ValidationStatus.NEED_CASTLING_STATE:
                context = (origin, dest, castling_state, grid_ctx)
                is_valid, new_castling = cls._is_valid_castle(*context)
                return None if is_valid else MoveStatus.INVALID, new_castling
            case ValidationStatus.NEED_PROMOTION_PIECE:
                return MoveStatus.REQUIRE_PROMOTION, None
            case _:
                return None, None

    @classmethod
    def _is_valid_move(cls, origin: Coord, dest: Coord, grid_ctx: GridContext) -> ValidationStatus:
        turn, grid = grid_ctx

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

        #missing data status
        if mov_case is MovSpecialCase.CASTLE:
            return ValidationStatus.NEED_CASTLING_STATE
        if cls._is_enpassant(o_piece, dest, mov_case, grid):
            return ValidationStatus.NEED_LAST_MOVE

        #pawn special cases
        if mov_case is MovSpecialCase.DOUBLE_PAWN_MOVE:
            if not cls._has_clear_path(origin, dest, grid) or d_piece is not None:
                return ValidationStatus.INVALID
        elif mov_case is MovSpecialCase.REQUIRES_OPPONENT and d_piece is None:
            return ValidationStatus.INVALID
        elif mov_case is MovSpecialCase.REQUIRES_EMPTY and d_piece is not None:
            return ValidationStatus.INVALID

        if o_piece.extendable_mov and not cls._has_clear_path(origin, dest, grid):
            return ValidationStatus.INVALID

        #movement does not leaves player in check


        # From here the move is valid
        if d_piece is not None and d_piece.type == PieceType.KING:
            return ValidationStatus.CHECKS_KING

        if cls._is_promotion(o_piece, dest, grid):
            return ValidationStatus.NEED_PROMOTION_PIECE

        return ValidationStatus.VALID

    @classmethod
    def _is_enpassant(cls, o_piece: Piece, dest: Coord, mov_case: MovSpecialCase,
                      grid: Grid) -> bool:
        """TODO
        """
        raise NotImplementedError()

    @classmethod
    def _is_promotion(cls, o_piece: Piece, dest: Coord, grid: Grid) -> bool:
        """TODO
        """
        #if o_piece.type != PieceType.PAWN:
        #    return False
        #if grid.get_at(dest) is not None:
        #    return False
        raise NotImplementedError()

    @classmethod
    def _has_clear_path(cls, origin: Coord, dest: Coord, grid: Grid) -> bool:
        """TODO
        """
        raise NotImplementedError()

    @classmethod
    def _is_valid_enpassant(cls, origin: Coord, dest: Coord, last_mov: Optional[Movement],
                           grid_ctx: GridContext) -> bool:
        """TODO
        """
        raise NotImplementedError()

    @classmethod
    def _is_valid_castle(cls, origin: Coord, dest: Coord, castling_state: CastlingState,
                           grid_ctx: GridContext) -> tuple[bool, CastlingState]:
        """TODO
        """
        raise NotImplementedError()

    @classmethod
    def get_board_state(cls, last_mov: Optional[Movement], castling_state: CastlingState,
                        grid_ctx: GridContext) -> TurnState:
        """TODO
        """
        turn, grid = grid_ctx
        context = (last_mov, castling_state, grid_ctx)

        pieces = grid.white_pieces if turn == SideColor.WHITE else grid.black_pieces
        opponent_pieces = grid.white_pieces if turn == SideColor.BLACK else grid.black_pieces
        king = [p for p in pieces if p.type == PieceType.KING][0]

        any_valid_move = any(cls._has_any_valid_move(context, p) for p in pieces)
        is_in_check = any(cls._attacks_coord(p, king, grid_ctx) for p in opponent_pieces)
        if is_in_check:
            if not any_valid_move:
                return TurnState.CHECKMATE
            return TurnState.CHECK
        if not any_valid_move:
            return TurnState.STALEMATE
        return TurnState.MOVE_TURN

    @classmethod
    def _attacks_coord(cls, piece: Piece, attacked_p: Piece, grid_ctx: GridContext) -> bool:
        origin = piece.coord
        destination = attacked_p.coord
        validation = cls._is_valid_move(origin, destination, grid_ctx)
        return validation in (ValidationStatus.VALID, ValidationStatus.CHECKS_KING)

    @classmethod
    def _has_any_valid_move(cls, context: tuple[Optional[Movement], CastlingState, GridContext],
                            piece: Piece) -> bool:
        for possible_mov in piece.movements:
            origin = piece.coord
            destination = Coord(origin.row-possible_mov.column, origin.column+possible_mov.row)
            invalid = cls.is_valid_move(origin, destination, *context)
            if invalid not in (None, MoveStatus.REQUIRE_PROMOTION):
                return False
        return True

    def get_max_extendable_movements(self, piece: Piece, direction: tuple[int, int], maxIterations: int) -> int:
        """Given a piece and direction, returns the number of movements it can perform without colliding, before reaching a given limit

        Args:
            piece (Piece): Piece to move.
            direction (tuple[int, int]): Direction of the extenable movement.
            maxIterations(int, optional): Maximum distance from piece origin.
            
        Returns:
           Int: Maximun number of movements in that direction.
        """
        
        i = 0
        row = piece.row
        column = piece.column

        while (row > -1 and row < 8) and (column > -1 and column < 8) and i < maxIterations:
            row += direction[0]
            column += direction[1]
            
            #If square is off board limits, or collided with a player piece return the previous square
            if row < 0 or row > 7 or column < 0  or column > 7 or self.is_player(row, column, piece.color):
                return i

            # If square is opponent return until this square
            if self.is_opponent(row, column, piece.color):
                return i+1
            
            i +=1
            
        return i

    def is_valid_movement(self, originRow: int, originColumn: int, destinationRow: int, destinationColumn: int) -> bool:
        """Determines whether the piece movement is valid or not

        Args:
            originRow (int): Origin row
            originColumn (int): Origin column
            destinationRow (int): Destination row
            destinationColumn (int): Destination column

        Returns:
            bool: Whether the movement is valid or not.
        """

        piece = self.__grid[originRow][originColumn]

        # If you try to move an empty square
        if piece.type == PieceType.EMPTY:
            return False

        # If you try to move an opponent square
        if self.is_opponent(originRow, originColumn, self.turn):
            return False

        # If the movement is an ilegal movement
        movement = (destinationRow, destinationColumn)
        playerPieces = self.whitePieces if self.turn == SideColor.WHITE else self.blackPieces
        if (movement not in self.get_valid_movements(piece)) if piece.type == PieceType.KING else (movement not in playerPieces[piece]):
            return False

        # If the movement leave you in check
        if self.in_check_after_mov(originRow, originColumn, destinationRow, destinationColumn):
            return False
        
        return True

    def attempt_move(self, origin_row: int, origin_column: int, destination_row: int, destination_column: int) -> tuple[bool, Optional[dict[str, Optional[Piece]]]]:
        """TODO
        """

        # Validat this movement
        if not self.is_valid_movement(origin_row,origin_column,destination_row,destination_column):
            return False, None

        eat_piece = self.__grid[destination_row][destination_column]

        # Perform movement
        piece = self.__grid[origin_row][origin_column]
        self.swap_pieces(origin_row,origin_column,destination_row,destination_column)        

        # Check for pawn special cases
        possible_en_passant = None
        if piece.type == PieceType.PAWN:
            # If move was enPassant
            if self.possibleEnPassant != None and self.possibleEnPassant[0] == destination_row and self.possibleEnPassant[1] == destination_column:
                eat_piece = self.__grid[destination_row-piece.moving_dir][destination_column]
            # If pawn performed doublemove, save it for en passant
            elif abs(destination_row-origin_row) == 2:
                possible_en_passant = (destination_row - piece.moving_dir, destination_column)
            # If pawn reached the last square it can move, promote it
            elif piece.row + piece.moving_dir == len(ROWS) or piece.row + piece.moving_dir == -1:
                self.remove_piece(piece.row, piece.column)

                if self.get_promotion_piece is None:
                    raise NotImplementedError("getPromotionPiece function not yet defined for board")

                new_piece = run(self.get_promotion_piece(piece.color, piece.row + piece.moving_dir, piece.column))
                new_piece.row = piece.row
                new_piece.column = piece.column
                self.add_piece(new_piece.row,new_piece.column, new_piece)

        elif piece.type == PieceType.KING:
            self.canCastleLeft = False
            self.canCastleRigth = False

            # If move was castle
            if abs(destination_column-origin_column) == 2:
                direction = (destination_column-origin_column)//abs(destination_column-origin_column)
                self.swap_pieces(origin_row, 0 if direction == -1 else 7, origin_row, destination_column - direction)

        self.possibleEnPassant = possible_en_passant

        # Eat opponent piece if it's eat move
        if eat_piece.type != PieceType.EMPTY:
            self.empty_square(eat_piece.row, eat_piece.column)

        # Pass turn and calculate new board conditions for next player
        self.turn = opponent(self.turn)
        self.squares_under_attack(opponent(self.turn))
        self.get_posible_turn_movements()
        self.set_game_state()

        return True, {
            'piece': piece,
            'eatPiece': eat_piece if eat_piece.type !=PieceType.EMPTY else None
        }

    def __init__(self) -> None:
        raise StaticClassInstanceError(ChessValidator)
