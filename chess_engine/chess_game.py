"""This module contains the model class game for handling Gameplay functionalities"""

# Import external libraries
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, cast

from chess_engine.chess_game_data import ChessGameData, GameState
# Import Internal modules
from chess_engine.structs import Coord
from chess_engine.grid import Grid
from chess_engine.piece import Piece, PieceType, SideColor
from chess_engine.chess_validator import ChessValidator, GridContext, TurnState
from utils.exceptions import InvalidChessGameError
from utils.utils import opponent


class MoveStatus(Enum):
    """TODO
    """
    PERFORMED = auto()
    GAME_ENDED = auto()
    INVALID = auto()
    REQUIRE_PROMOTION = auto()

@dataclass
class ChessGame():
    """TODO
    """

    grid: Grid
    data: ChessGameData
    validator: ChessValidator
    turn_state: TurnState = field(init=False)

    def __post_init__(self) -> None:
        self.turn_state = self.validator.get_board_state(self.grid_ctx())
        if not self.validator.is_valid_grid(self.grid_ctx()):
            raise InvalidChessGameError("Invalid grid")
        if not self.validator.is_valid_history(self.data.move_history, self.grid_ctx()):
            raise InvalidChessGameError("Invalid move history")

    def attempt_move(self, origin: Coord, destination: Coord) -> MoveStatus:
        """TODO
        """
        invalid = self._is_valid_move(origin, destination)
        if invalid is not None:
            return invalid

        o_piece, d_piece = self.grid.get_at(origin), self.grid.get_at(destination)
        o_piece = cast(Piece, o_piece)# Already validated origin indeed exists

        if self.validator.is_pawn_promotion(o_piece, destination, self.grid):
            return MoveStatus.REQUIRE_PROMOTION

        self._perform_move((origin, destination, o_piece, d_piece))
        return MoveStatus.PERFORMED

    def attempt_promotion(self, origin: Coord, destination: Coord,
                          piece_type: PieceType) -> MoveStatus:
        """TODO
        """
        invalid = self._is_valid_move(origin, destination)
        if invalid is not None:
            return invalid

        o_piece = self.grid.get_at(origin)
        prom_piece = Piece(piece_type, self.data.turn, destination)
        o_piece = cast(Piece, o_piece)# Already validated origin indeed exists

        self._perform_move((origin, destination, o_piece, prom_piece))

        # Next turn state
        self.turn_state = self.validator.get_board_state(self.opponent_grid_ctx())
        self.check_for_endgame()

        self.data.turn = opponent(self.data.turn)
        return MoveStatus.PERFORMED

    def _is_valid_move(self, origin: Coord, destination: Coord) -> Optional[MoveStatus]:
        if self.data.state != GameState.PENDING:
            return MoveStatus.GAME_ENDED

        last_mov = self.data.move_history[-1]
        if not self.validator.is_valid_move(origin, destination, last_mov, self.grid_ctx()):
            return MoveStatus.INVALID

        return None

    def _perform_move(self, context: tuple[Coord, Coord, Piece, Optional[Piece]]) -> None:
        origin, destination, o_piece, d_piece = context
        self.grid.swap_pieces(origin, destination)
        self.data.append_move(o_piece, destination if d_piece is None else d_piece)

    def _perform_promotion(self, context: tuple[Coord, Coord, Piece, Piece]) -> None:
        origin, destination, o_piece, prom_piece = context
        self.grid.set_at(origin, None)
        self.grid.set_at(destination, prom_piece)
        self.data.append_move(o_piece, prom_piece)

    def check_for_endgame(self) -> None:
        """TODO
        """
        if self.turn_state == TurnState.CHECK:
            self.turn_state = self.validator.is_checkmate(self.opponent_grid_ctx())
        else:
            self.turn_state = self.validator.is_stalemate(self.opponent_grid_ctx())

        if self.turn_state == TurnState.CHECKMATE:
            is_black_turn = self.data.turn == SideColor.BLACK
            player_won = GameState.BLACK_WIN if is_black_turn else GameState.WHITE_WIN
            self.data.state = player_won

        if self.turn_state == TurnState.STALEMATE:
            self.data.state = GameState.TIE

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
        validator = ChessValidator()
        return ChessGame(grid, game_data, validator)
