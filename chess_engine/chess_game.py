"""This module contains the model class game for handling Gameplay functionalities"""

# Import external libraries
from __future__ import annotations

from copy import copy
from dataclasses import dataclass, field
from typing import Optional, cast

from chess_engine.chess_game_data import ChessGameData, GameState, Movement
from chess_engine.chess_validator import (ChessValidator, GridContext,
                                          ValidationResult)
from chess_engine.enums import MoveStatus, TurnState
from chess_engine.grid import Grid
from chess_engine.piece import Piece, PieceType, SideColor
from chess_engine.structs import CastlingState, Coord, Dir
from utils.exceptions import InvalidChessGameError
from utils.utils import opponent


@dataclass
class ChessGame():
    """TODO
    """

    grid: Grid
    data: ChessGameData
    validate: bool = True
    turn_state: TurnState = field(init=False)

    def __post_init__(self) -> None:
        if self.validate:
            if not ChessValidator.is_valid_initial_grid():
                raise InvalidChessGameError("Invalid Initial Grid Constructor")
            valid_history, mov_grid_ctx = self._validate_history()
            if not valid_history:
                raise InvalidChessGameError("Invalid move history")
            if not self._validate_grid(mov_grid_ctx):
                raise InvalidChessGameError("Invalid grid")

        ChessValidator.clean_cache(self.grid_ctx())
        self._set_turn_state()

    def attempt_move(self, origin: Coord, destination: Coord) -> MoveStatus:
        """TODO
        """
        validation, new_castling, perform_castle = self._is_valid_move(origin, destination)
        if validation is not None:
            return validation

        o_piece, d_piece = self.grid.get_at(origin), self.grid.get_at(destination)
        o_piece = cast(Piece, o_piece)# Already validated origin indeed exists

        if perform_castle:
            self._perform_castle(origin.get_dir_to(destination))
        else:
            self._perform_move((origin, destination, o_piece, d_piece))

        ChessValidator.clean_cache(self.opponent_grid_ctx())

        # Next turn state
        self._set_castling(new_castling)
        self._set_turn_state()
        self._check_for_endgame()

        self.data.turn = opponent(self.data.turn)
        return MoveStatus.PERFORMED

    def attempt_promotion(self, origin: Coord, destination: Coord,
                          piece_type: PieceType) -> MoveStatus:
        """TODO
        """
        invalid, _, _ = self._is_valid_move(origin, destination)
        if invalid not in (None, MoveStatus.REQUIRE_PROMOTION):
            return invalid
        if not ChessValidator.is_valid_promotion_type(piece_type):
            return MoveStatus.INVALID

        o_piece = self.grid.get_at(origin)
        prom_piece = Piece(piece_type, self.data.turn, destination)
        o_piece = cast(Piece, o_piece)# Already validated origin indeed exists

        self._perform_promotion((origin, destination, o_piece, prom_piece))
        ChessValidator.clean_cache(self.opponent_grid_ctx())

        # Next turn state
        self._set_turn_state()
        self._check_for_endgame()

        self.data.turn = opponent(self.data.turn)
        return MoveStatus.PERFORMED

    def _is_valid_move(self, origin: Coord, destination: Coord) -> ValidationResult:
        if self.data.state != GameState.PENDING:
            return MoveStatus.INVALID, self._get_castling_state(), False

        last_mov = self._get_last_move()
        castling_state = self._get_castling_state()
        context = (last_mov, self.turn_state, castling_state, self.grid_ctx())
        return ChessValidator.is_valid_move(origin, destination, context)

    def _perform_move(self, context: tuple[Coord, Coord, Piece, Optional[Piece]]) -> None:
        origin, destination, o_piece, d_piece = context
        self.data.append_move(copy(o_piece), destination if d_piece is None else copy(d_piece))
        self.grid.swap_pieces(origin, destination)

    def _perform_castle(self, direction: Dir) -> None:
        w_row, b_row = ChessValidator.white_initial_row, ChessValidator.black_initial_row
        row = w_row if self.data.turn == SideColor.WHITE else b_row
        if direction.column < 0:
            self.grid.swap_pieces(Coord(row, 0), Coord(row, 3))
        else:
            self.grid.swap_pieces(Coord(row, 7), Coord(row, 5))

    def _set_castling(self, new_castling: CastlingState) -> None:
        if self.data.turn == SideColor.WHITE:
            self.data.white_castle = new_castling
        else:
            self.data.black_castle = new_castling

    def _perform_promotion(self, context: tuple[Coord, Coord, Piece, Piece]) -> None:
        origin, destination, o_piece, prom_piece = context
        self.data.append_move(copy(o_piece), copy(prom_piece))
        self.grid.set_at(origin, None)
        self.grid.set_at(destination, prom_piece)

    def _set_turn_state(self) -> None:
        last_mov = self._get_last_move()
        castling_state = self._get_castling_state()
        context = (last_mov, castling_state, self.opponent_grid_ctx())
        self.turn_state = ChessValidator.get_board_state(*context)

    def _check_for_endgame(self) -> None:
        if self.turn_state == TurnState.CHECKMATE:
            is_black_turn = self.data.turn == SideColor.BLACK
            player_won = GameState.BLACK_WIN if is_black_turn else GameState.WHITE_WIN
            self.data.state = player_won

        if self.turn_state == TurnState.STALEMATE:
            self.data.state = GameState.TIE

    def _validate_history(self) -> tuple[bool, GridContext]:
        grid = Grid.get_start_grid()
        game_data = ChessGameData.get_new_data()
        game_copy = ChessGame(grid, game_data, validate=False)
        for mov in self.data.move_history:
            origin = mov[0].coord
            destination = mov[1] if isinstance(mov[1], Coord) else mov[1].coord
            mov_status = game_copy.attempt_move(origin, destination)

            if mov_status is MoveStatus.INVALID:
                return False, game_copy.grid_ctx()
            if mov_status == MoveStatus.REQUIRE_PROMOTION:
                dest = cast(Piece, mov[1])
                prom_status = game_copy.attempt_promotion(origin, destination, dest.type)
                if prom_status != MoveStatus.PERFORMED:
                    return False, game_copy.grid_ctx()

        return True, game_copy.grid_ctx()

    def _validate_grid(self, mov_grid_ctx: GridContext) -> bool:
        return mov_grid_ctx[0] == self.data.turn and mov_grid_ctx[1] == self.grid

    def _get_last_move(self) -> Optional[Movement]:
        return self.data.move_history[-1] if len(self.data.move_history) > 0 else None

    def _get_castling_state(self) -> CastlingState:
        w_castle, b_castle = self.data.white_castle, self.data.black_castle
        return w_castle if self.data.turn == SideColor.WHITE else b_castle

    def grid_ctx(self) -> GridContext:
        """TODO
        """
        return (self.data.turn, self.grid)

    def opponent_grid_ctx(self) -> GridContext:
        """TODO
        """
        return (opponent(self.data.turn), self.grid)

    @classmethod
    def new_game(cls) -> ChessGame:
        """Returns a ChessGame from start

        Returns:
            ChessGame: ChessGame
        """
        grid = Grid.get_start_grid()
        game_data = ChessGameData.get_new_data()
        return ChessGame(grid, game_data)

    @classmethod
    def load_game(cls, grid: Grid, game_data: ChessGameData) -> ChessGame:
        """Returns a ChessGame from the provided data

        Returns:
            ChessGame: ChessGame
        """
        return ChessGame(grid, game_data)
