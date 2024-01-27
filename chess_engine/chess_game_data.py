"""TODO"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Optional, cast

from chess_engine.piece import Piece, SerPiece, SideColor
from chess_engine.structs import Coord
from serialization.serializable import Serializable
from utils.parseable_enum import ParseableEnum


class GameState(Enum, metaclass=ParseableEnum):
    """Enum for states in a chess game
    """
    PENDING = auto()
    WHITE_WIN = auto()
    BLACK_WIN = auto()
    TIE = auto()

Movement = tuple[Piece, Piece | Coord]
SerMovement = tuple[SerPiece, SerPiece | tuple[int,int]]
@dataclass
class ChessGameData(Serializable):
    """TODO
    """

    state: GameState
    turn: SideColor
    white_castle_left: bool
    white_castle_right: bool
    black_castle_left: bool
    black_castle_right: bool
    move_history: list[Movement]

    def append_move(self, piece: Piece, destination: Piece | Coord) -> None:
        """TODO
        """
        self.move_history.append((piece, destination))

    def get_serialization_attrs(self) -> dict[str, Any]:
        def serializable_move_history(move_history: list[Movement]) -> list[SerMovement]:
            ser_move_history: list[SerMovement] = []
            for piece, dest in move_history:
                ser_dest = (dest.row, dest.column) if isinstance(dest, Coord) else dest.serialize()
                ser_move_history.append((piece.serialize(), ser_dest))
            return ser_move_history

        return {
            "gameStatus"         : self.state.value,
            "turn"               : self.turn.value,
            "white_castle_left"  : self.white_castle_left,
            "white_castle_right" : self.white_castle_right,
            "black_castle_left"  : self.black_castle_left,
            "black_castle_right" :self.black_castle_right,
            "moveHistory" : serializable_move_history(self.move_history)
        }

    @classmethod
    def get_from_deserialize(cls, attrs: dict[str, Any], **kwargs: Any) -> ChessGameData:
        """TODO
        """
        def _parse_move_history(ser_move_history: list[SerMovement]) -> list[Movement]:
            def get_dest(ser_dest: SerPiece | tuple[int,int]) -> Optional[Piece] | Coord:
                match ser_dest:
                    case (_, (_, _)):
                        return Piece.deserialize(ser_dest)
                    case (_, _):
                        return Coord(*ser_dest)

            move_history: list[Movement] = []
            for ser_piece, ser_dest in ser_move_history:
                piece = Piece.deserialize(ser_piece)
                dest = get_dest(ser_dest)
                if piece is None or dest is None:
                    raise ValueError(f"Invalid piece {ser_piece} or destination \
                                     {ser_dest} in GameData deserialization")
                move_history.append((piece, dest))
            return move_history

        return ChessGameData(
            cast(GameState, GameState[attrs["gameStatus"]]),
            cast(SideColor, SideColor[attrs["turn"]]),
            attrs["white_castle_left"],
            attrs["white_castle_right"],
            attrs["black_castle_left"],
            attrs["black_castle_right"],
            _parse_move_history(attrs["moveHistory"])
            )
