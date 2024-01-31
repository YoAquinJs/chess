"""TODO"""

from enum import Enum, auto

from utils.parseable_enum import ParseableEnum


class SideColor(Enum, metaclass=ParseableEnum):
    """Enum for piece color
    """
    WHITE = 'w'
    BLACK = 'b'

class PieceType(Enum, metaclass=ParseableEnum):
    """Enum for each type of piece
    """
    PAWN = 'P'
    BISHOP = 'B'
    KNIGTH = 'K'
    ROOK = 'R'
    QUEEN = 'Q'
    KING = '@'

class MovSpecialCase(Enum):
    """Enum for each type of piece
    """
    NONE = auto()
    CASTLE = auto()
    DOUBLE_PAWN_MOVE = auto()
    IS_EMPTY = auto()

class ValidationStatus(Enum):
    """TODO
    """
    VALID = auto()
    CHECKS_KING = auto()
    INVALID = auto()
    NEED_LAST_MOVE = auto()
    NEED_CASTLING_STATE = auto()
    NEED_PROMOTION_PIECE = auto()

class MoveStatus(Enum):
    """TODO
    """
    PERFORMED = auto()
    INVALID = auto()
    REQUIRE_PROMOTION = auto()
    GAME_ALREADY_ENDED = auto()

class TurnState(Enum, metaclass=ParseableEnum):
    """Enum for states in a chess game
    """
    MOVE_TURN = auto()
    CHECK = auto()
    CHECKMATE = auto()
    STALEMATE = auto()

class GameState(Enum, metaclass=ParseableEnum):
    """Enum for states in a chess game
    """
    PENDING = auto()
    WHITE_WIN = auto()
    BLACK_WIN = auto()
    TIE = auto()
