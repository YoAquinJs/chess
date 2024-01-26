"""This module contains the model class game for handling Gameplay functionalities"""

# Import external libraries
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Optional, cast

from chess_engine.chess_game_data import ChessGameData
# Import Internal modules
from chess_engine.chess_validator import ChessValidator
from chess_engine.piece import Piece
from chess_engine.structs import Coord
from game_logic.consts import COLUMNS, ROWS, BoardState, PieceType, PlayerColor


@dataclass
class ChessGame():
    """TODO"""

    data: ChessGameData
    validator: ChessValidator

    async def get_promotion_piece(self, color: PlayerColor, row: int, column: int) -> Piece:
        """Asks the user for the promotion piece

        Args:
            color (PlayerColor): Piece color.
            row (int): Piece instantiation row.
            column (int): Piece instantiation column.

        Returns:
            Piece: Promotion Piece
        """

        piece_type: Optional[PieceType] = None
        while piece_type is None:
            try:
                piece_type = cast(PieceType, PieceType[input("Enter the promotion piece: ")])
                if piece_type == PieceType.KING:
                    piece_type = None
            except KeyError:
                print("Invalid type")

        return Piece(piece_type, color, row, column)

    def attempt_move(self, origin: Coord, destination: Coord) -> bool:
        """TODO
        """

        if self.status != GameStatus.PENDING:
            return False

        moved, move_inf = self.validator.attempt_move(movement[0], movement[1], movement[2], movement[3])
        if not moved:
            return False

        self.move_history.append((str(move_inf["piece"]), None if move_inf["eatPiece"] == None else str(move_inf["eatPiece"]), movement))

        if self.validator.boardState == BoardState.CHECKMATE:
            self.status = GameStatus.WHITE_WIN if self.validator.turn == PlayerColor.BLACK else GameStatus.BLACK_WIN  
        elif self.validator.boardState == BoardState.STALEMATE:
            self.status == GameStatus.STALEMATE

        return True

    @classmethod
    def new_game(cls) -> ChessGame:
        """Returns a ChessGame with all parameters to default

        Returns:
            ChessGame: ChessGame
        """
        
        #board = ChessValidator.start_board()
        #return cls(GameStatus.PENDING, board,)
