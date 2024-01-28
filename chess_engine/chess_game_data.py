"""TODO"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, cast
from chess_engine.enums import GameState

from chess_engine.piece import Piece, SerPiece, SideColor
from chess_engine.structs import CastlingState, Coord
from serialization.serializable import Serializable


Movement = tuple[Piece, Piece | Coord]
SerMovement = tuple[SerPiece, SerPiece | tuple[int,int]]
@dataclass
class ChessGameData(Serializable):
    """TODO
    """

    state: GameState
    turn: SideColor
    white_castle: CastlingState
    black_castle: CastlingState
    move_history: list[Movement]

    def append_move(self, piece: Piece, destination: Piece | Coord) -> None:
        """TODO
        """
        self.move_history.append((piece, destination))

    @staticmethod
    def get_new_data() -> ChessGameData:
        """TODO"""
        return ChessGameData(
            GameState.PENDING,
            SideColor.WHITE,
            CastlingState(True, True),
            CastlingState(True, True),
            []
            )

    def get_serialization_attrs(self) -> dict[str, Any]:
        def serializable_move_history(move_history: list[Movement]) -> list[SerMovement]:
            ser_move_history: list[SerMovement] = []
            for piece, dest in move_history:
                ser_dest = (dest.row, dest.column) if isinstance(dest, Coord) else dest.serialize()
                ser_move_history.append((piece.serialize(), ser_dest))
            return ser_move_history

        return {
            "gameStatus"    : self.state.value,
            "turn"          : self.turn.value,
            "whiteCastle_l" : self.white_castle.left,
            "whiteCastle_r" : self.white_castle.right,
            "blackCastle_l" : self.black_castle.left,
            "blackCastle_r" : self.black_castle.right,
            "moveHistory"   : serializable_move_history(self.move_history)
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
            CastlingState(attrs["whiteCastle_l"],attrs["whiteCastle_r"]),
            CastlingState(attrs["blackCastle_l"],attrs["blackCastle_r"]),
            _parse_move_history(attrs["moveHistory"])
            )
