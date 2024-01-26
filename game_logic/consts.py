"""This module contains constants for all subsystems of the app"""

#! This module shouldn't import from any other app module
from __future__ import annotations

from enum import Enum, auto
from os import getcwd, makedirs, path

from utils.parseable_enum import ParseableEnum

# Rendering Constants
SCREEN_SIZE = 4

# Serialization constants
MAX_GAMES_SAVED = 5

class AssetType(Enum):
    """Enum for assets types containing corresponding paths
    """
    SPRITE=path.join(getcwd(),"assets","sprites")
    AUDIO=path.join(getcwd(),"assets","audios")
    SAVINGS=path.join(getcwd(),"savings")

if not path.exists(AssetType.SAVINGS.value):
    makedirs(AssetType.SAVINGS.value)

class PrintColor(Enum):
    """Enum for console print colors
    """
    RED = '\033[31m'
    GREEN = '\033[32m'
    BLUE = '\033[96m'
    YELLOW = '\033[33m'
    RESET = '\033[0m'

class TestType(Enum, metaclass=ParseableEnum):
    """Enum for the multiple test type"""

    BOARD = auto()
    PIECE = auto()

# Unique identifiers for players, always a single character
class PlayerColor(Enum, metaclass=ParseableEnum):
    """Enum for piece color
    """
    WHITE = 'w'
    BLACK = 'b'

PLAYER_COLOR_INT = {
    PlayerColor.WHITE: 1,
    PlayerColor.BLACK: 2
}

# Unique identifiers for game states
class BoardState(Enum, metaclass=ParseableEnum):
    """Enum for states in a chess game
    """
    MOVE_TURN = auto()
    CHECK = auto()
    CHECKMATE = auto()
    STALEMATE = auto()

# Unique identifiers for pieces must be single character"
class PieceType(Enum, metaclass=ParseableEnum):
    """Enum for each type of piece
    """
    PAWN = 'P'
    BISHOP = 'B'
    KNIGTH = 'K'
    ROOK = 'R'
    QUEEN = 'Q'
    KING = '@'

PIECE_TYPE_INT = {
    PieceType.PAWN: 1,
    PieceType.BISHOP: 2,
    PieceType.KNIGTH: 3,
    PieceType.ROOK: 4,
    PieceType.QUEEN: 5,
    PieceType.KING: 6
}

class MovSpecialCase(Enum):
    """Enum for each type of piece
    """
    NONE = auto()
    CASTLE = auto()
    DOUBLE_PAWN_MOVE = auto()
    IS_EMPTY = auto()

# Constants for board
ROWS    = ['8','7','6','5','4','3','2','1']
COLUMNS = ['a','b','c','d','e','f','g','h']
BLACK_MOV_DIR = 1
WHITE_MOV_DIR = -1

BOARD_START = [
    ['bR', 'bK', 'bB', 'bQ', 'b@', 'bB', 'bK', 'bR'], # 8
    ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'], # 7
    ['##', '##', '##', '##', '##', '##', '##', '##'], # 6
    ['##', '##', '##', '##', '##', '##', '##', '##'], # 5
    ['##', '##', '##', '##', '##', '##', '##', '##'], # 4
    ['##', '##', '##', '##', '##', '##', '##', '##'], # 3
    ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'], # 2
    ['wR', 'wK', 'wB', 'wQ', 'w@', 'wB', 'wK', 'wR']  # 1
]#    a     b     c     d      e     f     g     h
