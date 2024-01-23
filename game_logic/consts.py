"""This module contains constants for all subsystems of the app"""

from __future__ import annotations

#! This module shouldn't import from any other app module
from enum import Enum, EnumMeta, auto
from os import getcwd, makedirs, path
from typing import cast

# Rendering Constants
SCREEN_SIZE = 4

# Serialization constants
MAX_GAMES_SAVED = 5

CHAR_SEPARATOR = 127
CHARACTER_ORDER = \
['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X',
 'Y','Z',
 'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x',
 'y','z',
 '.','-',',',':','+','\'','!','?','0','1','2','3','4','5','6','7','8','9','(',')','/','_','=','\\',
 '[',']','*','"','<','>',';']

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

# Meta Enum class for parsing from string value to Enum
class ParseableEnum(EnumMeta):
    """Makes a string parseable to the specified enum type
    """
    def __getitem__(cls, item: str) -> ParseableEnum:
        """This method parse from a string to the Enum object

        Args:
            item (str): The string to be parsed

        Returns:
            ParseableEnum: This enum
        """
        if item not in cls.__members__.keys():
            raise KeyError(f"No such value in {cls.__name__}: {item}")

        found = cls.__members__.get(item)
        return cast(ParseableEnum, found)

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
    EMPTY = '#'

PLAYER_COLOR_INT = {
    PlayerColor.EMPTY: 1,
    PlayerColor.WHITE: 2,
    PlayerColor.BLACK: 3
}

# Unique identifiers for game states
class GameResult(Enum, metaclass=ParseableEnum):
    """Enum for endding states in a chess game
    """
    PENDING = auto()
    WHITE_WIN = auto()
    BLACK_WIN = auto()
    STALEMATE = auto()
    TIE = auto()

class BoardState(Enum, metaclass=ParseableEnum):
    """Enum for states in a chess game
    """
    MVOE_TURN = auto()
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
    EMPTY = '#'

PIECE_TYPE_INT = {
    PieceType.EMPTY: 1,
    PieceType.PAWN: 2,
    PieceType.BISHOP: 3,
    PieceType.KNIGTH: 4,
    PieceType.ROOK: 5,
    PieceType.QUEEN: 6,
    PieceType.KING: 7
}

class MovSpecialCase(Enum):
    """Enum for each type of piece
    """
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
#     a     b     c     d      e     f     g     h
]
