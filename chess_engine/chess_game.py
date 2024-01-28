"""This module contains the model class game for handling Gameplay functionalities"""

# Import external libraries
from __future__ import annotations

from copy import copy
from dataclasses import dataclass, field
from typing import Optional, cast

from chess_engine.chess_game_data import ChessGameData, GameState
from chess_engine.chess_validator import ChessValidator, GridContext, TurnState
from chess_engine.enums import MoveStatus, ValidationStatus
from chess_engine.grid import Grid
from chess_engine.piece import Piece, PieceType, SideColor
# Import Internal modules
from chess_engine.structs import Coord
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
            valid_history, mov_grid_ctx = self.validate_history()
            if not valid_history:
                raise InvalidChessGameError("Invalid move history")
            if not self.validate_grid(mov_grid_ctx):
                raise InvalidChessGameError("Invalid grid")

        self.turn_state = ChessValidator.get_board_state(self.grid_ctx())

    def attempt_move(self, origin: Coord, destination: Coord) -> MoveStatus:
        """TODO
        """
        invalid = self._is_valid_move(origin, destination)
        if invalid is not None:
            return invalid

        o_piece, d_piece = self.grid.get_at(origin), self.grid.get_at(destination)
        o_piece = cast(Piece, o_piece)# Already validated origin indeed exists

        self._perform_move((origin, destination, o_piece, d_piece))
        return MoveStatus.PERFORMED

    def attempt_promotion(self, origin: Coord, destination: Coord,
                          piece_type: PieceType) -> MoveStatus:
        """TODO
        """
        invalid = self._is_valid_move(origin, destination)
        if invalid is not None and invalid != MoveStatus.REQUIRE_PROMOTION:
            return invalid

        o_piece = self.grid.get_at(origin)
        prom_piece = Piece(piece_type, self.data.turn, destination)
        o_piece = cast(Piece, o_piece)# Already validated origin indeed exists

        self._perform_promotion((origin, destination, o_piece, prom_piece))

        # Next turn state
        self.turn_state = ChessValidator.get_board_state(self.opponent_grid_ctx())
        self.check_for_endgame()

        self.data.turn = opponent(self.data.turn)
        return MoveStatus.PERFORMED

    def _is_valid_move(self, origin: Coord, destination: Coord) -> Optional[MoveStatus]:
        if self.data.state != GameState.PENDING:
            return MoveStatus.GAME_ALREADY_ENDED

        validation = ChessValidator.is_valid_move(origin, destination, self.grid_ctx())
        match validation:
            case ValidationStatus.INVALID:
                return MoveStatus.INVALID
            case ValidationStatus.NEED_LAST_MOVE:
                last_mov = self.data.move_history[-1] if len(self.data.move_history) > 0 else None
                context = (origin, destination, last_mov, self.grid_ctx())
                is_valid = ChessValidator.is_valid_enpassant(*context)
                return None if is_valid else MoveStatus.INVALID
            case ValidationStatus.NEED_CASTLING_STATE:
                w_castle, b_castle = self.data.white_castle, self.data.black_castle
                castling_state = w_castle if self.data.turn == SideColor.WHITE else b_castle
                context = (origin, destination, castling_state, self.grid_ctx())
                is_valid = ChessValidator.is_valid_castle(*context)
                return None if is_valid else MoveStatus.INVALID
            case ValidationStatus.NEED_PROMOTION_PIECE:
                return MoveStatus.REQUIRE_PROMOTION
            case _:
                return None

    def _perform_move(self, context: tuple[Coord, Coord, Piece, Optional[Piece]]) -> None:
        origin, destination, o_piece, d_piece = context
        self.data.append_move(copy(o_piece), destination if d_piece is None else copy(d_piece))
        self.grid.swap_pieces(origin, destination)

    def _perform_promotion(self, context: tuple[Coord, Coord, Piece, Piece]) -> None:
        origin, destination, o_piece, prom_piece = context
        self.data.append_move(copy(o_piece), copy(prom_piece))
        self.grid.set_at(origin, None)
        self.grid.set_at(destination, prom_piece)

    def check_for_endgame(self) -> None:
        """TODO
        """
        if self.turn_state == TurnState.CHECK:
            self.turn_state = ChessValidator.is_checkmate(self.opponent_grid_ctx())
        else:
            self.turn_state = ChessValidator.is_stalemate(self.opponent_grid_ctx())

        if self.turn_state == TurnState.CHECKMATE:
            is_black_turn = self.data.turn == SideColor.BLACK
            player_won = GameState.BLACK_WIN if is_black_turn else GameState.WHITE_WIN
            self.data.state = player_won

        if self.turn_state == TurnState.STALEMATE:
            self.data.state = GameState.TIE

    def validate_history(self) -> tuple[bool, GridContext]:
        """TODO
        """
        grid = Grid.get_start_grid()
        game_data = ChessGameData.get_new_data()
        game_copy = ChessGame(grid, game_data, validate=False)
        for mov in self.data.move_history:
            origin = mov[0].coord
            destination = mov[1] if isinstance(mov[1], Coord) else mov[1].coord
            mov_status = game_copy.attempt_move(origin, destination)

            if mov_status == MoveStatus.INVALID:
                return False, game_copy.grid_ctx()
            if mov_status == MoveStatus.REQUIRE_PROMOTION:
                dest = cast(Piece, mov[1])
                prom_status = game_copy.attempt_promotion(origin, destination, dest.type)
                if prom_status != MoveStatus.PERFORMED:
                    return False, game_copy.grid_ctx()

        return True, game_copy.grid_ctx()

    def validate_grid(self, mov_grid_ctx: GridContext) -> bool:
        """TODO
        """
        return mov_grid_ctx[0] == self.data.turn and mov_grid_ctx[1] == self.grid

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
