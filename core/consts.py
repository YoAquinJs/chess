"""This module contains constants for all subsystems of the app"""

#! This module shouldn't import from any other app module
from os import getcwd, makedirs, path
from enum import Enum, EnumMeta

# Rendering Constants
SCREEN_SIZE = 4

# Serialization constants
SPRITE = f"{getcwd()}/assets/sprites/"
AUDIO = f"{getcwd()}/assets/audios/"
SAVINGS = f"{getcwd()}/savings/"
MAX_GAMES_SAVED = 5

if not path.exists(SAVINGS):
    makedirs(SAVINGS)

class InputType(Enum):
    bool='bool'
    int='int'
    str='str'

class PrintColor(Enum):
    """Enum for console print colors"""
    
    red = '\033[31m'
    green = '\033[32m'
    blue = '\033[96m'
    yellow = '\033[33m'
    reset = '\033[0m'

class GameScreen(Enum):
    """Enum for game screens in the game"""
    
    mainMenu = 'move_turn'
    loadGame = 'loadGame'
    onGame = 'on_game'

# Meta Enum class for parsing from string value to Enum
class ParseableEnum(EnumMeta):
    def __getitem__(cls, item: str) -> object:
        """This method parse from a string to the Enum object

        Args:
            item (str): The string to be parsed

        Returns:
            object: This enum
        """
        
        match = None
        for member in cls.__members__.values():
            if member.value == item:
                match = member
                break
        
        if match is None:
            raise KeyError(f"No such value in {cls.__name__}: {item}")
        
        return match

class TestType(Enum, metaclass=ParseableEnum):
    """Enum for the multiple test type"""

    board = 'board'
    piece = 'piece'

# Unique identifiers for players, always a single character
class PlayerColor(Enum, metaclass=ParseableEnum):
    """Enum for piece color"""

    white = 'w'
    black = 'b'
    empty = '#'

PLAYERCOLORINT = {
    PlayerColor.empty: 1,
    PlayerColor.white: 2,
    PlayerColor.black: 3
}

# Unique identifiers for game states
class GameResult(Enum, metaclass=ParseableEnum):
    """Enum for endding states in a chess game"""

    pending = 'pending'
    whiteWin = 'whiteWin'
    blackWin = 'blackWin'
    stalemate = 'stalemate'
    tie = 'tie'

class BoardState(Enum, metaclass=ParseableEnum):
    """Enum for states in a chess game"""

    moveTurn = 'moveTurn'
    check = 'check'
    checkmate = 'checkmate'
    stalemate = 'stalemate'

# Unique identifiers for pieces, always a single character, the format it's f"{PlayerColor}{PieceType}"
class PieceType(Enum, metaclass=ParseableEnum):
    """Enum for each type of piece"""

    pawn = 'P'
    bishop = 'B'
    knigth = 'K'
    rook = 'R'
    queen = 'Q'
    king = '@'
    empty = '#'

PIECETYPEINT = {
    PieceType.empty: 1,
    PieceType.pawn: 2,
    PieceType.bishop: 3,
    PieceType.knigth: 4,
    PieceType.rook: 5,
    PieceType.queen: 6,
    PieceType.king: 7
}

# It's assumed you can never move to a square with a piece of your own
class MovementSpecialCase(Enum):
    """Enum for each type of piece"""

    castle = 'canCastle'
    isEmpty = 'isEmpty'
    doublePawnMove = 'doublePawnMove'

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
# The start board has type List[List[str]], when used, the board class converts it to List[List[Piece]]
